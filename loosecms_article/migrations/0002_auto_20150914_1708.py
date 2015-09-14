# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=loosecms.fields.LoosecmsTaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='utime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='ArticleCategory',
        ),
    ]
