# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0006_auto_20150922_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(help_text='Give the name of the article.', max_length=200, verbose_name='title')),
                ('body', loosecms.fields.LoosecmsRichTextField(verbose_name='body')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='loosecms_article.Article', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'loosecms_article_article_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'article Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
