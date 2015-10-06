# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0010_auto_20151006_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemanager',
            name='category_page',
            field=models.BooleanField(default=True, help_text='Check this box if you want to show all categories in this pageor show instant the articles', verbose_name='show category page'),
        ),
    ]
