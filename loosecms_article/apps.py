# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LooseCMSArticleConfig(AppConfig):
    name = 'loosecms_article'
    verbose_name = _('Loose CMS Plugin - Article')
