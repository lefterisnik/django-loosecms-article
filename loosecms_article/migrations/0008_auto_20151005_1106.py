# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
from django.core.exceptions import ObjectDoesNotExist


def forwards_func(apps, schema_editor):
    Article = apps.get_model('loosecms_article', 'Article')
    ArticleTranslation = apps.get_model('loosecms_article', 'ArticleTranslation')

    for object in Article.objects.all():
        ArticleTranslation.objects.create(
            master_id=object.pk,
            language_code=settings.LANGUAGE_CODE,
            title=object.title,
            body=object.body
        )


def backwards_func(apps, schema_editor):
    Article = apps.get_model('loosecms_article', 'Article')
    ArticleTranslation = apps.get_model('loosecms_article', 'ArticleTranslation')

    for object in Article.objects.all():
        translation = _get_translation(object, ArticleTranslation)
        object.title = translation.title
        object.body = translation.body
        object.save()   # Note this only calls Model.save() in South.


def _get_translation(object, ArticleTranslation):
    translations = ArticleTranslation.objects.filter(master_id=object.pk)
    try:
        # Try default translation
        return translations.get(language_code=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            # Try default language
            return translations.get(language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Hope there is a single translation
            return translations.get()

class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0007_auto_20151005_1106'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]