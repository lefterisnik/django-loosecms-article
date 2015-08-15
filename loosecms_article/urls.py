# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

app_urlpatterns = [
    url(r'^syndication/(?P<manager_pk>[0-9]+)/$', NewsFeed(), name='syndication'),
]

urlpatterns = []