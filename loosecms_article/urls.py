# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

from loosecms.views import detail

app_urlpatterns = [
    url(r'^syndication/(?P<manager_pk>[0-9]+)/$', NewsFeed(), name='syndication'),
]

urlpatterns = [
     url(r'^article-category/(?P<category_slug>[0-9A-Za-z-_.]+)/$', detail, name='article-category-info')
]