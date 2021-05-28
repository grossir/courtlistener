# Generated by Django 3.1.7 on 2021-05-28 19:23

import django.db.models.deletion
import localflavor.us.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BarMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barMembership', localflavor.us.models.USStateField(max_length=2, verbose_name='the two letter state abbreviation of a bar membership')),
            ],
            options={
                'verbose_name': 'bar membership',
                'ordering': ['barMembership'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stub_account', models.BooleanField(default=False)),
                ('employer', models.CharField(blank=True, help_text="the user's employer", max_length=100, null=True)),
                ('address1', models.CharField(blank=True, max_length=100, null=True)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=2, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=10, null=True)),
                ('avatar', models.ImageField(blank=True, help_text="the user's avatar", upload_to='avatars/%Y/%m/%d')),
                ('wants_newsletter', models.BooleanField(default=False, help_text='This user wants newsletters')),
                ('unlimited_docket_alerts', models.BooleanField(default=False, help_text='Should the user get unlimited docket alerts?')),
                ('plaintext_preferred', models.BooleanField(default=False, help_text='should the alert should be sent in plaintext')),
                ('activation_key', models.CharField(max_length=40)),
                ('key_expires', models.DateTimeField(blank=True, help_text="The time and date when the user's activation_key expires", null=True)),
                ('email_confirmed', models.BooleanField(default=False, help_text='The user has confirmed their email address')),
                ('notes', models.TextField(blank=True, help_text='Any notes about the user.')),
                ('is_tester', models.BooleanField(default=False, help_text='The user tests new features before they are finished')),
                ('barmembership', models.ManyToManyField(blank=True, to='users.BarMembership', verbose_name='the bar memberships held by the user')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='the user this model extends')),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
        ),
    ]
