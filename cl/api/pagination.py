from base64 import b64decode, b64encode
from collections import namedtuple
from urllib.parse import parse_qs, urlencode

from django.conf import settings
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
from rest_framework.pagination import BasePagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param


class ShallowOnlyPageNumberPagination(PageNumberPagination):
    """A paginator that blocks deep pagination

    Thank you MuckRock for this contribution.
    """

    max_pagination_depth = 100

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            msg = "Invalid page: That page number is not an integer"
            raise NotFound(msg)

        if page_number > self.max_pagination_depth:
            msg = "Invalid page: Deep API pagination is not allowed. Please review API documentation."
            raise NotFound(msg)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class TinyAdjustablePagination(ShallowOnlyPageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class MediumAdjustablePagination(ShallowOnlyPageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"


class BigPagination(ShallowOnlyPageNumberPagination):
    page_size = 300


Cursor = namedtuple("Cursor", ["search_after", "reverse"])


class ESCursorPagination(BasePagination):
    """Custom pagination class to handle ES cursor pagination, based in the ES
    search_after param.
    """

    def __init__(self):
        self.page_size = settings.SEARCH_API_PAGE_SIZE
        self.request = None
        self.es_list_instance = None
        self.results_count = None
        self.results_in_page = None
        self.base_url = None
        self.cursor = None
        self.cursor_query_param = "cursor"
        self.invalid_cursor_message = "Invalid cursor"

    def paginate_queryset(self, es_list_instance, request, view=None):
        """Paginate the Elasticsearch query and retrieve the results."""

        self.base_url = request.build_absolute_uri()

        self.request = request
        self.cursor = self.decode_cursor(request)

        self.es_list_instance = es_list_instance
        self.es_list_instance.set_pagination(self.cursor, self.page_size)
        results = self.es_list_instance.get_paginated_results()
        self.results_in_page = len(results)
        self.results_count = results.hits.total.value
        return results

    def get_paginated_response(self, data):
        """Generate a custom paginated response using the data provided."""
        return Response(
            {
                "count": self.get_results_count(),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_next_link(self):
        """Constructs the URL for the next page based on the current page's
        last item.
        """
        search_after_sort_key = (
            self.es_list_instance.get_search_after_sort_key()
        )
        if not self.has_next(search_after_sort_key):
            return None

        cursor = Cursor(search_after=search_after_sort_key, reverse=False)
        return self.encode_cursor(cursor)

    def get_previous_link(self):
        """Constructs the URL for the next page based on the current page's
        last item.
        """
        reverse_search_after_sort_key = (
            self.es_list_instance.get_reverse_search_after_sort_key()
        )
        if not self.has_prev(reverse_search_after_sort_key):
            return None

        cursor = Cursor(
            search_after=reverse_search_after_sort_key, reverse=True
        )
        return self.encode_cursor(cursor)

    def decode_cursor(self, request):
        """Given a request with a cursor, return a `Cursor` instance."""
        encoded = request.query_params.get(self.cursor_query_param)
        if encoded is None:
            return None
        try:
            querystring = b64decode(encoded.encode("ascii")).decode("ascii")
            tokens = parse_qs(querystring, keep_blank_values=True)
            search_after = tokens.get("s", None)
            reverse = tokens.get("r", ["0"])[0]
            reverse = bool(int(reverse))

        except (TypeError, ValueError):
            raise NotFound(self.invalid_cursor_message)
        return Cursor(search_after=search_after, reverse=reverse)

    def encode_cursor(self, cursor):
        """Given a Cursor instance, return an url with encoded cursor."""
        tokens = {}
        if cursor.search_after != 0:
            tokens["s"] = cursor.search_after
        if cursor.reverse:
            tokens["r"] = "1"

        querystring = urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode("ascii")).decode("ascii")
        return replace_query_param(
            self.base_url, self.cursor_query_param, encoded
        )

    def get_results_count(self):
        """Provides a structured count of results based on settings.

        :return: A dictionary containing "exact" count and whether there are
        "more" or equal results than ELASTICSEARCH_MAX_RESULT_COUNT.
        """
        return {
            "exact": (
                self.results_count
                if self.results_count
                <= settings.ELASTICSEARCH_MAX_RESULT_COUNT
                else settings.ELASTICSEARCH_MAX_RESULT_COUNT
            ),
            "more": self.results_count
            > settings.ELASTICSEARCH_MAX_RESULT_COUNT,
        }

    def has_next(self, search_after_sort_key):
        """Determines if there is a next page based on the search_after key
        and results count.
        """
        if search_after_sort_key is None:
            return False
        if self.results_in_page < self.page_size:
            return False
        return True

    def has_prev(self, search_after_sort_key):
        """Determines if there is a next page based on the search_after key
        and results count.
        """
        return True
