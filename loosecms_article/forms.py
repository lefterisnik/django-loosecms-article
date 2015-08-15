# -*- coding:utf-8 -*-
from django import forms
from .models import ArticleManager, NewsArticleManager
from loosecms.forms import PluginForm


class ArticleManagerForm(PluginForm):

    class Meta(PluginForm.Meta):
        model = ArticleManager


class NewsArticleManagerForm(PluginForm):
    interval = forms.IntegerField(localize=False, min_value=0, max_value=32767)

    class Meta(PluginForm.Meta):
        model = NewsArticleManager