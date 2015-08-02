# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.core.urlresolvers import reverse
from .models import Article


class NewsFeed(Feed):
    feed_type = Rss201rev2Feed
    description_template = 'rss/rss.html'
    title = _('News')
    link = '/news/'
    description = _('News')
    author_name = _('Article')

    def items(self):
        return Article.objects.filter(published=True).order_by('-ctime')[:10]

    def get_context_data(self, **kwargs):
        context = super(NewsFeed, self).get_context_data(**kwargs)
        return context

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('full-info', args=[item.manager.page.slug, item.category.slug, item.slug] )