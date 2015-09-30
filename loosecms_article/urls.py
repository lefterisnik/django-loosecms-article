# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

from loosecms.views import detail

urlpatterns = [
    url(r'^articles/syndication/(?P<manager_pk>[0-9]+)/$', NewsFeed(), name='article-syndication'),
]

embed_urlpatterns = [
     url(r'^(?P<slug>[0-9A-Za-z-_.]+)/$', detail, name='info'),
     url(r'^article-category/(?P<category_slug>[0-9A-Za-z-_.]+)/$', detail, name='article-category-info'),
]