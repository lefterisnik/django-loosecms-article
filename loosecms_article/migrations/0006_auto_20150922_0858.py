# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0005_auto_20150922_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemanager',
            name='slug',
            field=models.SlugField(help_text='Give the slug of the article manager.', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='newsarticlemanager',
            name='slug',
            field=models.SlugField(help_text='Give the slug of the article news manager.', unique=True, verbose_name='slug'),
        ),
    ]
