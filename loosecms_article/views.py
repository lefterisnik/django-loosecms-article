# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Article, NewsArticleManager


class NewsFeed(Feed):
    feed_type = Rss201rev2Feed
    description_template = 'rss/rss.html'

    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(NewsArticleManager, pk=kwargs['manager_pk'])

    def items(self, obj):
        if obj.manager:
            return Article.objects.filter(published=True, manager=obj.manager).order_by('-ctime')[:obj.number]
        else:
            return Article.objects.filter(published=True).order_by('-ctime')[:obj.number]

    def title(self, obj):
        return obj.rss_title

    def description(self, obj):
        return obj.rss_description

    def link(self, obj):
        if obj.manager:
            return obj.manager.page.slug
        else:
            return ''

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('info', args=[item.manager.page.slug, item.slug] )
