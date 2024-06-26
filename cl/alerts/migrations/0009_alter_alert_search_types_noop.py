# Generated by Django 5.0.5 on 2024-04-25 21:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("alerts", "0008_add_scheduled_alert_hit_and_alert_type_to_alert"),
    ]

    operations = [
        migrations.AlterField(
            model_name="alert",
            name="alert_type",
            field=models.CharField(
                choices=[
                    ("o", "Opinions"),
                    ("r", "RECAP"),
                    ("d", "RECAP Dockets"),
                    ("rd", "RECAP Documents"),
                    ("oa", "Oral Arguments"),
                    ("p", "People"),
                    ("pa", "Parenthetical"),
                ],
                default="o",
                help_text="The type of search alert this is, one of: o (Opinions), r (RECAP), d (RECAP Dockets), rd (RECAP Documents), oa (Oral Arguments), p (People), pa (Parenthetical)",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="alertevent",
            name="alert_type",
            field=models.CharField(
                choices=[
                    ("o", "Opinions"),
                    ("r", "RECAP"),
                    ("d", "RECAP Dockets"),
                    ("rd", "RECAP Documents"),
                    ("oa", "Oral Arguments"),
                    ("p", "People"),
                    ("pa", "Parenthetical"),
                ],
                default="o",
                help_text="The type of search alert this is, one of: o (Opinions), r (RECAP), d (RECAP Dockets), rd (RECAP Documents), oa (Oral Arguments), p (People), pa (Parenthetical)",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="realtimequeue",
            name="item_type",
            field=models.CharField(
                choices=[
                    ("o", "Opinions"),
                    ("r", "RECAP"),
                    ("d", "RECAP Dockets"),
                    ("rd", "RECAP Documents"),
                    ("oa", "Oral Arguments"),
                    ("p", "People"),
                    ("pa", "Parenthetical"),
                ],
                db_index=True,
                help_text="the type of item this is, one of: o (Opinions), r (RECAP), d (RECAP Dockets), rd (RECAP Documents), oa (Oral Arguments), p (People), pa (Parenthetical)",
                max_length=3,
            ),
        ),
    ]
