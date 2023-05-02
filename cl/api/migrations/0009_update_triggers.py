# Generated by Django 3.2.18 on 2023-03-17 23:21

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_add_event_tables_and_triggers'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='webhook',
            name='snapshot_insert',
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name='webhook',
            name='snapshot_update',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='webhook',
            trigger=pgtrigger.compiler.Trigger(
                name='update_or_delete_snapshot_update',
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition='WHEN (OLD."id" IS DISTINCT FROM NEW."id" OR OLD."date_created" IS DISTINCT FROM NEW."date_created" OR OLD."user_id" IS DISTINCT FROM NEW."user_id" OR OLD."event_type" IS DISTINCT FROM NEW."event_type" OR OLD."url" IS DISTINCT FROM NEW."url" OR OLD."enabled" IS DISTINCT FROM NEW."enabled" OR OLD."version" IS DISTINCT FROM NEW."version" OR OLD."failure_count" IS DISTINCT FROM NEW."failure_count")',
                    func='INSERT INTO "api_webhookhistoryevent" ("date_created", "date_modified", "enabled", "event_type", "failure_count", "id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "url", "user_id", "version") VALUES (OLD."date_created", OLD."date_modified", OLD."enabled", OLD."event_type", OLD."failure_count", OLD."id", _pgh_attach_context(), NOW(), \'update_or_delete_snapshot\', OLD."id", OLD."url", OLD."user_id", OLD."version"); RETURN NULL;',
                    hash='dcb7a3c78b3f87bf30bec2e8d5f72093459f5155',
                    operation='UPDATE',
                    pgid='pgtrigger_update_or_delete_snapshot_update_224f9',
                    table='api_webhook', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='webhook',
            trigger=pgtrigger.compiler.Trigger(
                name='update_or_delete_snapshot_delete',
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "api_webhookhistoryevent" ("date_created", "date_modified", "enabled", "event_type", "failure_count", "id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "url", "user_id", "version") VALUES (OLD."date_created", OLD."date_modified", OLD."enabled", OLD."event_type", OLD."failure_count", OLD."id", _pgh_attach_context(), NOW(), \'update_or_delete_snapshot\', OLD."id", OLD."url", OLD."user_id", OLD."version"); RETURN NULL;',
                    hash='7fd87ef311025e2f62355b94e83ae846fb8b639b',
                    operation='DELETE',
                    pgid='pgtrigger_update_or_delete_snapshot_delete_7e421',
                    table='api_webhook', when='AFTER')),
        ),
    ]