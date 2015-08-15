# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .models import Article, ArticleManager, NewsArticleManager


class NewsFeed(Feed):
    feed_type = Rss201rev2Feed
    description_template = 'rss/rss.html'
    title = _('News')
    link = '/news/'
    description = _('News')
    author_name = _('Article')

    def get_object(self, request, manager_pk):
        return get_object_or_404(NewsArticleManager, pk=manager_pk)

    def items(self, obj):
        if obj.manager:
            return Article.objects.filter(published=True, manager=obj.manager).order_by('-ctime')[:10]
        else:
            return Article.objects.filter(published=True).order_by('-ctime')[:10]

    def title(self, obj):
        return obj.rss_title

    def description(self, obj):
        return obj.rss_description

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('info', args=[item.manager.page.slug, item.category.slug, item.slug] )
