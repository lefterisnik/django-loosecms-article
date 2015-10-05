# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_article', '0008_auto_20151005_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='body',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title',
        ),
    ]
