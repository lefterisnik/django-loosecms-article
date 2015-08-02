# -*- coding:utf-8 -*-
from .models import ArticleManager, NewsArticleManager
from loosecms.forms import PluginForm


class ArticleManagerForm(PluginForm):

    class Meta(PluginForm.Meta):
        model = ArticleManager


class NewsArticleManagerForm(PluginForm):

    class Meta(PluginForm.Meta):
        model = NewsArticleManager