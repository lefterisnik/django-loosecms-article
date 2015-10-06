# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0009_auto_20151005_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=loosecms.fields.LoosecmsTaggableManager(to='loosecms.LoosecmsTag', through='loosecms.LoosecmsTagged', help_text='A comma-separated list of tags.', verbose_name='category'),
        ),
    ]
