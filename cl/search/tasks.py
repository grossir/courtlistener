import logging
import socket
from datetime import timedelta
from typing import Any

import scorched
import waffle
from celery import Task
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from elasticsearch.exceptions import (
    NotFoundError,
    RequestError,
    TransportError,
)
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document, UpdateByQuery, connections
from requests import Session
from scorched.exc import SolrError

from cl.audio.models import Audio
from cl.celery_init import app
from cl.lib.elasticsearch_utils import es_index_exists
from cl.lib.search_index_utils import InvalidDocumentError
from cl.people_db.models import Person, Position
from cl.search.documents import (
    ES_CHILD_ID,
    AudioDocument,
    DocketDocument,
    ESRECAPDocument,
    PersonDocument,
    PositionDocument,
)
from cl.search.models import (
    SEARCH_TYPES,
    Docket,
    OpinionCluster,
    RECAPDocument,
)
from cl.search.types import (
    ESDocumentClassType,
    ESDocumentInstanceType,
    ESModelType,
    SaveDocumentResponseType,
)

models_alert_support = [Audio]

logger = logging.getLogger(__name__)


@app.task
def add_items_to_solr(item_pks, app_label, force_commit=False):
    """Add a list of items to Solr

    :param item_pks: An iterable list of item PKs that you wish to add to Solr.
    :param app_label: The type of item that you are adding.
    :param force_commit: Whether to send a commit to Solr after your addition.
    This is generally not advised and is mostly used for testing.
    """
    search_dicts = []
    model = apps.get_model(app_label)
    items = model.objects.filter(pk__in=item_pks).order_by()
    for item in items:
        try:
            if model in [OpinionCluster, Docket]:
                # Dockets make a list of items; extend, don't append
                search_dicts.extend(item.as_search_list())
            else:
                search_dicts.append(item.as_search_dict())
        except AttributeError as e:
            print(f"AttributeError trying to add: {item}\n  {e}")
        except ValueError as e:
            print(f"ValueError trying to add: {item}\n  {e}")
        except InvalidDocumentError:
            print(f"Unable to parse: {item}")

    with Session() as session:
        si = scorched.SolrInterface(
            settings.SOLR_URLS[app_label], http_connection=session, mode="w"
        )
        try:
            si.add(search_dicts)
            if force_commit:
                si.commit()
        except (socket.error, SolrError) as exc:
            add_items_to_solr.retry(exc=exc, countdown=30)
        else:
            # Mark dockets as updated if needed
            if model == Docket:
                items.update(date_modified=now(), date_last_index=now())


@app.task(ignore_resutls=True)
def add_or_update_recap_docket(
    data, force_commit=False, update_threshold=60 * 60
):
    """Add an entire docket to Solr or update it if it's already there.

    This is an expensive operation because to add or update a RECAP docket in
    Solr means updating every document that's a part of it. So if a docket has
    10,000 documents, we'll have to pull them *all* from the database, and
    re-index them all. It'd be nice to not have to do this, but because Solr is
    de-normalized, every document in the RECAP Solr index has a copy of every
    field in Solr. For example, if the name of the case changes, that has to get
    reflected in every document in the docket in Solr.

    To deal with this mess, we have a field on the docket that says when we last
    updated it in Solr. If that date is after a threshold, we just don't do the
    update unless we know the docket has something new.

    :param data: A dictionary containing the a key for 'docket_pk' and
    'content_updated'. 'docket_pk' will be used to find the docket to modify.
    'content_updated' is a boolean indicating whether the docket must be
    updated.
    :param force_commit: Whether to send a commit to Solr (this is usually not
    needed).
    :param update_threshold: Items staler than this number of seconds will be
    updated. Items fresher than this number will be a no-op.
    """
    if data is None:
        return

    with Session() as session:
        si = scorched.SolrInterface(
            settings.SOLR_RECAP_URL, http_connection=session, mode="w"
        )
        some_time_ago = now() - timedelta(seconds=update_threshold)
        d = Docket.objects.get(pk=data["docket_pk"])
        too_fresh = d.date_last_index is not None and (
            d.date_last_index > some_time_ago
        )
        update_not_required = not data.get("content_updated", False)
        if all([too_fresh, update_not_required]):
            return
        else:
            try:
                si.add(d.as_search_list())
                if force_commit:
                    si.commit()
            except SolrError as exc:
                add_or_update_recap_docket.retry(exc=exc, countdown=30)
            else:
                d.date_last_index = now()
                d.save()


@app.task
def add_docket_to_solr_by_rds(item_pks, force_commit=False):
    """Add RECAPDocuments from a single Docket to Solr.

    This is a performance enhancement that can be used when adding many RECAP
    Documents from a single docket to Solr. Instead of pulling the same docket
    metadata for these items over and over (adding potentially thousands of
    queries on a large docket), just pull the metadata once and cache it for
    every document that's added.

    :param item_pks: RECAPDocument pks to add or update in Solr.
    :param force_commit: Whether to send a commit to Solr (this is usually not
    needed).
    :return: None
    """
    with Session() as session:
        si = scorched.SolrInterface(
            settings.SOLR_RECAP_URL, http_connection=session, mode="w"
        )
        rds = RECAPDocument.objects.filter(pk__in=item_pks).order_by()
        try:
            metadata = rds[0].get_docket_metadata()
        except IndexError:
            metadata = None

        try:
            si.add(
                [item.as_search_dict(docket_metadata=metadata) for item in rds]
            )
            if force_commit:
                si.commit()
        except SolrError as exc:
            add_docket_to_solr_by_rds.retry(exc=exc, countdown=30)


@app.task
def delete_items(items, app_label, force_commit=False):
    with Session() as session:
        si = scorched.SolrInterface(
            settings.SOLR_URLS[app_label], http_connection=session, mode="w"
        )
        try:
            si.delete_by_ids(list(items))
            if force_commit:
                si.commit()
        except SolrError as exc:
            delete_items.retry(exc=exc, countdown=30)


def person_first_time_indexing(parent_id: int, position: Position) -> None:
    """Index a person and their no judiciary positions into Elasticsearch.

    It creates a parent document for the person and indexes each non-judiciary
    position as a child document.

    :param parent_id: The ID of the Person.
    :param position: A Position instance.
    :return: None
    """

    # Create the parent document if it does not exist yet in ES
    person_doc = PersonDocument()
    doc = person_doc.prepare(position.person)
    PersonDocument(meta={"id": parent_id}, **doc).save(
        skip_empty=False, return_doc_meta=True
    )

    # After indexing the person, look for non-judicial positions that have not
    # been indexed and index them.
    person_positions = Position.objects.filter(person_id=parent_id)
    non_judicial_positions = [
        pos for pos in person_positions if not pos.is_judicial_position
    ]
    for person_position in non_judicial_positions:
        doc_id = ES_CHILD_ID(person_position.pk).POSITION
        if PositionDocument.exists(id=doc_id):
            continue

        position_doc = PositionDocument()
        pos_doc = position_doc.prepare(person_position)
        es_args = {
            "_routing": parent_id,
            "meta": {"id": doc_id},
        }
        PositionDocument(**es_args, **pos_doc).save(
            skip_empty=False,
            return_doc_meta=False,
            refresh=settings.ELASTICSEARCH_DSL_AUTO_REFRESH,
        )


@app.task(
    bind=True,
    autoretry_for=(TransportError, ConnectionError, RequestError),
    max_retries=3,
    interval_start=5,
)
def save_document_in_es(
    self: Task,
    instance: ESModelType,
    es_document: ESDocumentClassType,
) -> SaveDocumentResponseType | None:
    """Save a document in Elasticsearch using a provided callable.

    :param self: The celery task
    :param instance: The instance of the document to save.
    :param es_document: A Elasticsearch DSL document.
    :return: SaveDocumentResponseType or None
    """
    es_args = {}
    if isinstance(instance, Position):
        parent_id = getattr(instance.person, "pk", None)
        if not all(
            [
                es_index_exists(es_document._index._name),
                parent_id,
                # avoid indexing position records if the parent is not a judge
                instance.person.is_judge,
            ]
        ):
            return
        if not PersonDocument.exists(id=parent_id):
            person_first_time_indexing(parent_id, instance)

        doc_id = ES_CHILD_ID(instance.pk).POSITION
        es_args["_routing"] = parent_id
    elif isinstance(instance, Person):
        # index person records only if they were ever a judge.
        if not instance.is_judge:
            return
        doc_id = instance.pk
    elif isinstance(instance, RECAPDocument):
        parent_id = getattr(instance.docket_entry.docket, "pk", None)
        if not all(
            [
                es_index_exists(es_document._index._name),
                parent_id,
            ]
        ):
            return

        if not DocketDocument.exists(id=parent_id):
            # create the parent document if it does not exist in ES
            docket_doc = DocketDocument()
            doc = docket_doc.prepare(instance.docket_entry.docket)
            DocketDocument(meta={"id": parent_id}, **doc).save(
                skip_empty=False, return_doc_meta=True
            )
        doc_id = ES_CHILD_ID(instance.pk).RECAP
        es_args["_routing"] = parent_id
    else:
        doc_id = instance.pk

    es_args["meta"] = {"id": doc_id}
    es_doc = es_document()
    doc = es_doc.prepare(instance)
    response = es_document(**es_args, **doc).save(
        skip_empty=False,
        return_doc_meta=True,
        refresh=settings.ELASTICSEARCH_DSL_AUTO_REFRESH,
    )
    if type(instance) in models_alert_support and response["_version"] == 1:
        # Only send search alerts when a new instance of a model that support
        # Alerts is indexed in ES _version:1
        if es_document == AudioDocument and not waffle.switch_is_active(
            "oa-es-alerts-active"
        ):
            # Disable ES Alerts if oa-es-alerts-active switch is not enabled
            self.request.chain = None
            return None
        return response["_id"], doc
    else:
        self.request.chain = None
        return None


@app.task(
    bind=True,
    autoretry_for=(TransportError, ConnectionError, RequestError),
    max_retries=3,
    interval_start=5,
)
def update_document_in_es(
    self: Task,
    es_document: ESDocumentInstanceType,
    fields_values_to_update: dict[str, Any],
) -> None:
    """Update a document in Elasticsearch.
    :param self: The celery task
    :param es_document: The instance of the document to save.
    :param fields_values_to_update: A dictionary with fields and values to update.
    :return: None
    """

    Document.update(
        es_document,
        **fields_values_to_update,
        refresh=settings.ELASTICSEARCH_DSL_AUTO_REFRESH,
    )


@app.task(
    bind=True,
    autoretry_for=(
        TransportError,
        ConnectionError,
        RequestError,
        NotFoundError,
    ),
    max_retries=3,
    interval_start=5,
)
def update_child_documents_by_query(
    self: Task,
    es_document: ESDocumentClassType,
    parent_instance: ESModelType,
    fields_to_update: list[str],
    fields_map: dict[str, str] | None = None,
) -> None:
    """Update child documents in Elasticsearch in bulk using the UpdateByQuery
    API.

    :param self: The celery task
    :param es_document: The Elasticsearch Document type to update.
    :param parent_instance: The parent instance containing the fields to update.
    :param fields_to_update: List of field names to be updated.
    :param fields_map: A mapping from model fields to Elasticsearch document fields.
    :return: None
    """

    s = es_document.search()
    main_doc = None
    if es_document is PositionDocument:
        s = s.query("parent_id", type="position", id=parent_instance.pk)
        main_doc = PersonDocument.get(id=parent_instance.pk)
    elif es_document is ESRECAPDocument:
        s = s.query("parent_id", type="recap_document", id=parent_instance.pk)
        main_doc = DocketDocument.get(id=parent_instance.pk)

    if not main_doc:
        return

    if not main_doc:
        # Abort bulk update for a not supported document.
        return
    client = connections.get_connection()
    ubq = UpdateByQuery(using=client, index=es_document._index._name).query(
        s.to_dict()["query"]
    )

    script_lines = []
    params = {}
    for field_to_update in fields_to_update:
        field_list = (
            fields_map[field_to_update] if fields_map else [field_to_update]
        )
        for field_name in field_list:
            script_lines.append(
                f"ctx._source.{field_name} = params.{field_name};"
            )
            prepare_method = getattr(main_doc, f"prepare_{field_name}", None)
            if prepare_method:
                params[field_name] = prepare_method(parent_instance)
            else:
                params[field_name] = getattr(parent_instance, field_to_update)
    script_source = "\n".join(script_lines)
    # Build the UpdateByQuery script and execute it
    ubq = ubq.script(source=script_source, params=params)
    ubq.execute()

    if settings.ELASTICSEARCH_DSL_AUTO_REFRESH:
        # Set auto-refresh, used for testing.
        es_document._index.refresh()


@app.task(
    bind=True,
    autoretry_for=(
        TransportError,
        ConnectionError,
        RequestError,
        NotFoundError,
    ),
    max_retries=3,
    interval_start=5,
)
def index_docket_parties_in_es(
    self: Task,
    docket_id: int,
) -> None:
    """Update a document in Elasticsearch.
    :param self: The celery task
    :param docket_id: The docket ID to update in ES.
    :param fields_values_to_update: A dictionary with fields and values to update.
    :return: None
    """

    docket_document = DocketDocument.get(id=docket_id)
    docket = Docket.objects.get(id=docket_id)
    parties_prepared = docket_document.prepare_parties(docket)

    fields_to_update = {
        key: list(set_values) for key, set_values in parties_prepared.items()
    }
    Document.update(
        docket_document,
        **fields_to_update,
        refresh=settings.ELASTICSEARCH_DSL_AUTO_REFRESH,
    )


@app.task(
    bind=True,
    autoretry_for=(TransportError, ConnectionError, RequestError),
    max_retries=3,
    interval_start=5,
)
def index_parent_and_child_docs(
    self: Task,
    instance_id: int,
    search_type: str,
) -> None:
    """Index parent and child documents in Elasticsearch.

    :param self: The Celery task instance
    :param instance_id: The parent instance ID.
    :param search_type: The Search Type to index parent and child docs.
    :return: None
    """
    match search_type:
        case SEARCH_TYPES.PEOPLE:
            instance = Person.objects.prefetch_related("positions").get(
                pk=instance_id
            )
            parent_es_document = PersonDocument
            child_es_document = PositionDocument
            child_id_property = "POSITION"
            child_docs = instance.positions.all()
        case SEARCH_TYPES.RECAP:
            instance = Docket.objects.get(pk=instance_id)
            parent_es_document = DocketDocument
            child_es_document = ESRECAPDocument
            child_id_property = "RECAP"
            child_docs = RECAPDocument.objects.filter(
                docket_entry__docket=instance
            )
        case _:
            return

    doc = parent_es_document().prepare(instance)
    es_args = {
        "meta": {"id": instance_id},
    }
    response = parent_es_document(**es_args, **doc).save(
        skip_empty=False,
        return_doc_meta=False,
        refresh=settings.ELASTICSEARCH_DSL_AUTO_REFRESH,
    )
    if response != "created":
        model_label = parent_es_document.Django.model.__name__.capitalize()
        logger.error(
            f"The {model_label} with ID:{instance_id} can't be index in ES. "
            "Aborting the indexing of their child objects."
        )
        return

    client = connections.get_connection()
    base_doc = {
        "_op_type": "index",
        "_index": parent_es_document._index._name,
    }
    child_docs_to_index = []
    for child in child_docs.iterator():
        child_doc = child_es_document().prepare(child)
        child_params = {
            "_id": getattr(ES_CHILD_ID(child.pk), child_id_property),
            "_routing": f"{instance_id}",
        }
        child_doc.update(base_doc)
        child_doc.update(child_params)
        child_docs_to_index.append(child_doc)

    # Perform bulk indexing for child documents
    bulk(client, child_docs_to_index)
    if settings.ELASTICSEARCH_DSL_AUTO_REFRESH:
        # Set auto-refresh, used for testing.
        parent_es_document._index.refresh()
