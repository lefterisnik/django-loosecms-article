# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib import admin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *

from loosecms.plugin_pool import plugin_pool
from loosecms.plugin_modeladmin import PluginModelAdmin


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1
    prepopulated_fields = {'slug': ('title', )}


class ArticlePlugin(PluginModelAdmin):
    model = ArticleManager
    name = _('Articles')
    form = ArticleManagerForm
    plugin = True
    template = "plugin/articles.html"
    inlines = [
        ArticleInline,
    ]
    extra_initial_help = None
    fields = ('type', 'placeholder', 'title', 'number', 'page', 'hide_categories', 'published')

    def update_context(self, context, manager):
        categories = ArticleCategory.objects.filter(article__manager=manager).annotate(article_count=Count('article'))
        if 'kwargs' in context:
            if 'slug' in context['kwargs']:
                context['slug'] = context['kwargs']['slug']
                context['category_slug'] = context['kwargs']['category_slug']
                '''Fetch specific article'''
                try:
                    articles = Article.objects.select_related().get(published=True, slug=context['slug'])
                except Article.DoesNotExist:
                    raise Http404
            elif 'category_slug' in context['kwargs']:
                context['category_slug'] = context['kwargs']['category_slug']

                '''Fetch all articles for requested category'''
                articles = Article.objects.select_related().filter(published=True, category__slug=context['category_slug']).order_by('-ctime')
                if len(articles) == 0:
                    raise Http404

        elif context['page_slug'] != '':
            ''' Fetch all articles for requested page'''
            articles = Article.objects.select_related().filter(published=True).order_by('-ctime')

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

    def get_changeform_initial_data(self, request):
        initial = {}
        if self.extra_initial_help:
            initial['type'] = self.extra_initial_help['type']
            initial['placeholder'] = self.extra_initial_help['placeholder']
            initial['page'] = self.extra_initial_help['page']

            return initial
        else:
            return {'type': 'ArticlePlugin'}


class NewsArticlePlugin(PluginModelAdmin):
    model = NewsArticleManager
    name = _('Recent Articles')
    form = NewsArticleManagerForm
    plugin = True
    template = "plugin/new_articles.html"
    extra_initial_help = None
    fieldsets = (
        (None, {
            'fields': ('type', 'placeholder', 'title', 'number', 'published')
        }),
        ('Advanced options', {
            'fields': ('manager', 'header_title', 'interval')
        }),
        ('Rss options', {
            'fields': ('rss', ('rss_title', 'rss_description'))
        }),
    )

    def update_context(self, context, manager):
        if manager.manager:
            newsarticles = Article.objects.select_related().\
                               filter(published=True, manager=manager.manager).\
                               order_by('-ctime')[:manager.number]
        else:
            newsarticles = Article.objects.select_related().\
                               filter(published=True).\
                               order_by('-ctime')[:manager.number]

        context['newsarticles'] = newsarticles
        context['newsarticlemanager'] = manager
        return context

    def get_changeform_initial_data(self, request):
        initial = {}
        if self.extra_initial_help:
            initial['type'] = self.extra_initial_help['type']
            initial['placeholder'] = self.extra_initial_help['placeholder']

            return initial
        else:
            return {'type': 'NewsArticlePlugin'}

plugin_pool.register_plugin(ArticlePlugin)
plugin_pool.register_plugin(NewsArticlePlugin)