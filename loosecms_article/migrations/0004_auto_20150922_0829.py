# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0003_article_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemanager',
            name='title',
            field=models.CharField(help_text='Give the name of the article manager.', unique=True, max_length=200, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='newsarticlemanager',
            name='title',
            field=models.CharField(help_text='Give the name of the article news manager.', unique=True, max_length=200, verbose_name='title'),
        ),
    ]
