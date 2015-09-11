# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Give the name of the article.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the article, to create the url of the article.', unique=True, verbose_name='slug')),
                ('body', loosecms.fields.LoosecmsRichTextField(verbose_name='body')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='ctime')),
                ('utime', models.DateTimeField(auto_now=True, verbose_name='utime')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Give the name of the category.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the category, to create the url of the articles which refers to this.', unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleManager',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the article manager.', max_length=200, verbose_name='title')),
                ('number', models.IntegerField(help_text='Give the number of articles per page.', null=True, verbose_name='number', blank=True)),
                ('hide_categories', models.BooleanField(default=False, help_text='Select if you want to hide the category list view.', verbose_name='hide categories list')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('page', models.ForeignKey(verbose_name='page', to='loosecms.HtmlPage', help_text='Select the page which this article manager will showed. Is needed to know the page of the article manager to create the unique article urls.')),
            ],
            bases=('loosecms.plugin',),
        ),
        migrations.CreateModel(
            name='NewsArticleManager',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the article news manager.', max_length=200, verbose_name='title')),
                ('number', models.IntegerField(help_text='Give the number of articles rendering by this manager', verbose_name='number')),
                ('header_title', models.CharField(default='Recent articles', help_text='Give the title of the panel which articles will appeared.', max_length=150, verbose_name='header title')),
                ('rss', models.BooleanField(default=False, help_text='Check this box if you want to appear the rss link in the header.', verbose_name='rss')),
                ('rss_title', models.CharField(help_text='Give the title of the rss feed.', max_length=200, verbose_name='rss title', blank=True)),
                ('rss_description', models.CharField(help_text='Give a small description for the rss feed.', max_length=200, verbose_name='rss description', blank=True)),
                ('interval', models.PositiveSmallIntegerField(default=2000, help_text='Set the change rate in miliseconds.', verbose_name='interval')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(blank=True, to='loosecms_article.ArticleManager', help_text='Select the article manager that contain the request articles. In case of no selection all artilces form all managers will be included.', null=True, verbose_name='manager')),
            ],
            bases=('loosecms.plugin',),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='category', to='loosecms_article.ArticleCategory', help_text='Select the category of this article.'),
        ),
        migrations.AddField(
            model_name='article',
            name='manager',
            field=models.ForeignKey(verbose_name='manager', to='loosecms_article.ArticleManager', help_text='Select the article manager of this article.'),
        ),
    ]
