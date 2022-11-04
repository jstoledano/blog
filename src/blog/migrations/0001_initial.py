# Generated by Django 4.1.3 on 2022-11-03 20:53

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Name of the category. Max length is 255.', max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(help_text='Slug of the category. Max length is 255.', max_length=60, unique=True, verbose_name='Slug')),
                ('icon', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_html', models.TextField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('summary', models.TextField(blank=True, verbose_name='Summary')),
                ('body', models.TextField(blank=True, verbose_name='Body')),
                ('extend', models.TextField(blank=True, verbose_name='Extend')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now)),
                ('summary_html', models.TextField(blank=True, editable=False)),
                ('summary_meta', models.TextField(blank=True, editable=False)),
                ('body_html', models.TextField(blank=True, editable=False)),
                ('extend_html', models.TextField(blank=True, editable=False)),
                ('enable_comments', models.BooleanField(default=True)),
                ('cover', models.URLField(blank=True)),
                ('slug', models.SlugField(unique_for_date='pub_date')),
                ('status', models.IntegerField(choices=[(1, 'Live'), (2, 'Draft'), (3, 'Hidden')], default=1)),
                ('featured', models.BooleanField(default=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='entradas', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_category', to='blog.category')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
                'ordering': ['-id', '-pub_date'],
                'get_latest_by': 'pub_date',
                'unique_together': {('slug', 'category')},
            },
        ),
    ]
