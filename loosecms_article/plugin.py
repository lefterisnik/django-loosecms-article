# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#from taggit.models import Tag

from .models import *

from loosecms.plugin_pool import plugin_pool
from loosecms.plugin_modeladmin import PluginModelAdmin
from loosecms.models import LoosecmsTag

from parler.admin import TranslatableStackedInline


class ArticleInline(TranslatableStackedInline):
    model = Article
    extra = 1
    fields = ('title', 'slug', 'body', 'category', 'manager', 'published')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}


class ArticleManagerPlugin(PluginModelAdmin):
    model = ArticleManager
    name = _('Article Container')
    plugin = True
    template = "plugin/articles.html"
    inlines = [
        ArticleInline,
    ]
    prepopulated_fields = {'slug': ('title', )}

    def update_context(self, context, manager):
        categories = LoosecmsTag.objects.filter(article__manager=manager).annotate(article_count=Count('article'))
        if 'slug' in context:
            '''Fetch specific article'''
            try:
                articles = Article.objects.select_related()\
                    .get(published=True, slug=context['slug'], manager=manager)
            except Article.DoesNotExist:
                raise Http404
        elif 'category_slug' in context:
            '''Fetch all articles for requested category'''
            articles = Article.objects.select_related()\
                .filter(published=True, category__slug=context['category_slug'], manager=manager)\
                .order_by('-ctime')
            if len(articles) == 0:
                raise Http404
        else:
            ''' Fetch all articles for requested page'''
            articles = Article.objects.select_related()\
                .filter(published=True, manager=manager)\
                .order_by('-ctime')

        if isinstance(articles, QuerySet):
            paginator = Paginator(articles, manager.number)
            pageset = context['request'].GET.get('pageset')
            try:
                articles = paginator.page(pageset)
            except PageNotAnInteger:
                articles = paginator.page(1)
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)

        context['categories'] = categories
        context['articles'] = articles
        context['articlemanager'] = manager
        return context


class NewsArticleManagerPlugin(PluginModelAdmin):
    model = NewsArticleManager
    name = _('Recent Article Container')
    plugin = True
    template = "plugin/new_articles.html"
    fieldsets = (
        (None, {
            'fields': ('type', 'placeholder', 'title', 'number', 'published')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('manager', 'header_title', 'interval')
        }),
        ('Rss options', {
            'classes': ('collapse',),
            'fields': ('rss', 'rss_title', 'rss_description')
        }),
    )

    def update_context(self, context, manager):
        if manager.manager:
            newsarticles = Article.objects.select_related('manager__page').\
                               filter(published=True, manager=manager.manager).\
                               order_by('-ctime')[:manager.number]
        else:
            newsarticles = Article.objects.select_related('manager__page').\
                               filter(published=True).\
                               order_by('-ctime')[:manager.number]

        context['newsarticles'] = newsarticles
        context['newsarticlemanager'] = manager
        return context

plugin_pool.register_plugin(ArticleManagerPlugin)
plugin_pool.register_plugin(NewsArticleManagerPlugin)