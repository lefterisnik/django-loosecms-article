# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.text import slugify
from django.db import models, migrations

try:
    from unidecode import unidecode
except ImportError:
    unidecode = lambda slug: slug


def generate_slug_articlemanager(apps, schema_editor):
    ArticleManager = apps.get_model('loosecms_article', 'ArticleManager')
    for articlemanager in ArticleManager.objects.all():
        articlemanager.slug = slugify(unidecode(articlemanager.title))
        articlemanager.save()


def generate_slug_newsarticlemanager(apps, schema_editor):
    NewsArticleManager = apps.get_model('loosecms_article', 'NewsArticleManager')
    for newsarticlemanager in NewsArticleManager.objects.all():
        newsarticlemanager.slug = slugify(unidecode(newsarticlemanager.title))
        newsarticlemanager.save()


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0004_auto_20150922_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemanager',
            name='slug',
            field=models.SlugField(help_text='Give the slug of the article manager.', verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='newsarticlemanager',
            name='slug',
            field=models.SlugField(help_text='Give the slug of the article news manager.', verbose_name='slug'),
        ),
        migrations.RunPython(generate_slug_articlemanager),
        migrations.RunPython(generate_slug_newsarticlemanager),
    ]