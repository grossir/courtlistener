# Generated by Django 5.0.2 on 2024-05-31 21:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audio", "0006_audio_update_sources_noop"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audio",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("C", "court website"),
                    ("R", "public.resource.org"),
                    ("CR", "court website merged with resource.org"),
                    ("L", "lawbox"),
                    ("LC", "lawbox merged with court"),
                    ("LR", "lawbox merged with resource.org"),
                    ("LCR", "lawbox merged with court and resource.org"),
                    ("M", "manual input"),
                    ("A", "internet archive"),
                    ("H", "brad heath archive"),
                    ("Z", "columbia archive"),
                    ("ZA", "columbia merged with internet archive"),
                    ("ZD", "columbia merged with direct court input"),
                    ("ZC", "columbia merged with court"),
                    ("ZH", "columbia merged with brad heath archive"),
                    ("ZLC", "columbia merged with lawbox and court"),
                    ("ZLR", "columbia merged with lawbox and resource.org"),
                    (
                        "ZLCR",
                        "columbia merged with lawbox, court, and resource.org",
                    ),
                    ("ZR", "columbia merged with resource.org"),
                    ("ZCR", "columbia merged with court and resource.org"),
                    ("ZL", "columbia merged with lawbox"),
                    ("ZM", "columbia merged with manual input"),
                    ("ZQ", "columbia merged with 2020 anonymous database"),
                    (
                        "U",
                        "Harvard, Library Innovation Lab Case Law Access Project",
                    ),
                    ("CU", "court website merged with Harvard"),
                    ("D", "direct court input"),
                    ("Q", "2020 anonymous database"),
                    ("QU", "2020 anonymous database merged with Harvard"),
                    ("CU", "court website merged with Harvard"),
                    (
                        "CRU",
                        "court website merged with public.resource.org and Harvard",
                    ),
                    ("DU", "direct court input merged with Harvard"),
                    ("LU", "lawbox merged with Harvard"),
                    ("LCU", "Lawbox merged with court website and Harvard"),
                    (
                        "LRU",
                        "Lawbox merged with public.resource.org and with Harvard",
                    ),
                    ("MU", "Manual input merged with Harvard"),
                    ("RU", "public.resource.org merged with Harvard"),
                    ("ZU", "columbia archive merged with Harvard"),
                    ("ZLU", "columbia archive merged with Lawbox and Harvard"),
                    (
                        "ZDU",
                        "columbia archive merged with direct court input and Harvard",
                    ),
                    (
                        "ZLRU",
                        "columbia archive merged with lawbox, public.resource.org and Harvard",
                    ),
                    (
                        "ZLCRU",
                        "columbia archive merged with lawbox, court website, public.resource.org and Harvard",
                    ),
                    (
                        "ZCU",
                        "columbia archive merged with court website and Harvard",
                    ),
                    (
                        "ZMU",
                        "columbia archive merged with manual input and Harvard",
                    ),
                    (
                        "ZRU",
                        "columbia archive merged with public.resource.org and Harvard",
                    ),
                    (
                        "ZLCU",
                        "columbia archive merged with lawbox, court website and Harvard",
                    ),
                    ("G", "recap"),
                ],
                help_text="the source of the audio file, one of: C (court website), R (public.resource.org), CR (court website merged with resource.org), L (lawbox), LC (lawbox merged with court), LR (lawbox merged with resource.org), LCR (lawbox merged with court and resource.org), M (manual input), A (internet archive), H (brad heath archive), Z (columbia archive), ZA (columbia merged with internet archive), ZD (columbia merged with direct court input), ZC (columbia merged with court), ZH (columbia merged with brad heath archive), ZLC (columbia merged with lawbox and court), ZLR (columbia merged with lawbox and resource.org), ZLCR (columbia merged with lawbox, court, and resource.org), ZR (columbia merged with resource.org), ZCR (columbia merged with court and resource.org), ZL (columbia merged with lawbox), ZM (columbia merged with manual input), ZQ (columbia merged with 2020 anonymous database), U (Harvard, Library Innovation Lab Case Law Access Project), CU (court website merged with Harvard), D (direct court input), Q (2020 anonymous database), QU (2020 anonymous database merged with Harvard), CU (court website merged with Harvard), CRU (court website merged with public.resource.org and Harvard), DU (direct court input merged with Harvard), LU (lawbox merged with Harvard), LCU (Lawbox merged with court website and Harvard), LRU (Lawbox merged with public.resource.org and with Harvard), MU (Manual input merged with Harvard), RU (public.resource.org merged with Harvard), ZU (columbia archive merged with Harvard), ZLU (columbia archive merged with Lawbox and Harvard), ZDU (columbia archive merged with direct court input and Harvard), ZLRU (columbia archive merged with lawbox, public.resource.org and Harvard), ZLCRU (columbia archive merged with lawbox, court website, public.resource.org and Harvard), ZCU (columbia archive merged with court website and Harvard), ZMU (columbia archive merged with manual input and Harvard), ZRU (columbia archive merged with public.resource.org and Harvard), ZLCU (columbia archive merged with lawbox, court website and Harvard), G (recap)",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="audioevent",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("C", "court website"),
                    ("R", "public.resource.org"),
                    ("CR", "court website merged with resource.org"),
                    ("L", "lawbox"),
                    ("LC", "lawbox merged with court"),
                    ("LR", "lawbox merged with resource.org"),
                    ("LCR", "lawbox merged with court and resource.org"),
                    ("M", "manual input"),
                    ("A", "internet archive"),
                    ("H", "brad heath archive"),
                    ("Z", "columbia archive"),
                    ("ZA", "columbia merged with internet archive"),
                    ("ZD", "columbia merged with direct court input"),
                    ("ZC", "columbia merged with court"),
                    ("ZH", "columbia merged with brad heath archive"),
                    ("ZLC", "columbia merged with lawbox and court"),
                    ("ZLR", "columbia merged with lawbox and resource.org"),
                    (
                        "ZLCR",
                        "columbia merged with lawbox, court, and resource.org",
                    ),
                    ("ZR", "columbia merged with resource.org"),
                    ("ZCR", "columbia merged with court and resource.org"),
                    ("ZL", "columbia merged with lawbox"),
                    ("ZM", "columbia merged with manual input"),
                    ("ZQ", "columbia merged with 2020 anonymous database"),
                    (
                        "U",
                        "Harvard, Library Innovation Lab Case Law Access Project",
                    ),
                    ("CU", "court website merged with Harvard"),
                    ("D", "direct court input"),
                    ("Q", "2020 anonymous database"),
                    ("QU", "2020 anonymous database merged with Harvard"),
                    ("CU", "court website merged with Harvard"),
                    (
                        "CRU",
                        "court website merged with public.resource.org and Harvard",
                    ),
                    ("DU", "direct court input merged with Harvard"),
                    ("LU", "lawbox merged with Harvard"),
                    ("LCU", "Lawbox merged with court website and Harvard"),
                    (
                        "LRU",
                        "Lawbox merged with public.resource.org and with Harvard",
                    ),
                    ("MU", "Manual input merged with Harvard"),
                    ("RU", "public.resource.org merged with Harvard"),
                    ("ZU", "columbia archive merged with Harvard"),
                    ("ZLU", "columbia archive merged with Lawbox and Harvard"),
                    (
                        "ZDU",
                        "columbia archive merged with direct court input and Harvard",
                    ),
                    (
                        "ZLRU",
                        "columbia archive merged with lawbox, public.resource.org and Harvard",
                    ),
                    (
                        "ZLCRU",
                        "columbia archive merged with lawbox, court website, public.resource.org and Harvard",
                    ),
                    (
                        "ZCU",
                        "columbia archive merged with court website and Harvard",
                    ),
                    (
                        "ZMU",
                        "columbia archive merged with manual input and Harvard",
                    ),
                    (
                        "ZRU",
                        "columbia archive merged with public.resource.org and Harvard",
                    ),
                    (
                        "ZLCU",
                        "columbia archive merged with lawbox, court website and Harvard",
                    ),
                    ("G", "recap"),
                ],
                help_text="the source of the audio file, one of: C (court website), R (public.resource.org), CR (court website merged with resource.org), L (lawbox), LC (lawbox merged with court), LR (lawbox merged with resource.org), LCR (lawbox merged with court and resource.org), M (manual input), A (internet archive), H (brad heath archive), Z (columbia archive), ZA (columbia merged with internet archive), ZD (columbia merged with direct court input), ZC (columbia merged with court), ZH (columbia merged with brad heath archive), ZLC (columbia merged with lawbox and court), ZLR (columbia merged with lawbox and resource.org), ZLCR (columbia merged with lawbox, court, and resource.org), ZR (columbia merged with resource.org), ZCR (columbia merged with court and resource.org), ZL (columbia merged with lawbox), ZM (columbia merged with manual input), ZQ (columbia merged with 2020 anonymous database), U (Harvard, Library Innovation Lab Case Law Access Project), CU (court website merged with Harvard), D (direct court input), Q (2020 anonymous database), QU (2020 anonymous database merged with Harvard), CU (court website merged with Harvard), CRU (court website merged with public.resource.org and Harvard), DU (direct court input merged with Harvard), LU (lawbox merged with Harvard), LCU (Lawbox merged with court website and Harvard), LRU (Lawbox merged with public.resource.org and with Harvard), MU (Manual input merged with Harvard), RU (public.resource.org merged with Harvard), ZU (columbia archive merged with Harvard), ZLU (columbia archive merged with Lawbox and Harvard), ZDU (columbia archive merged with direct court input and Harvard), ZLRU (columbia archive merged with lawbox, public.resource.org and Harvard), ZLCRU (columbia archive merged with lawbox, court website, public.resource.org and Harvard), ZCU (columbia archive merged with court website and Harvard), ZMU (columbia archive merged with manual input and Harvard), ZRU (columbia archive merged with public.resource.org and Harvard), ZLCU (columbia archive merged with lawbox, court website and Harvard), G (recap)",
                max_length=10,
            ),
        ),
    ]
