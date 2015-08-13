# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from loosecms.models import Plugin, HtmlPage
from ckeditor.fields import RichTextField


class ArticleManager(Plugin):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the article manager.'))
    number = models.IntegerField(_('number'), null=True, blank=True,
                                 help_text=_('Give the number of articles per page.'))
    page = models.ForeignKey(HtmlPage, verbose_name=_('page'),
                             limit_choices_to={'is_template': False},
                             help_text=_('Select the page which this article manager will showed. Is needed to know '
                                         'the page of the article manager to create the unique article urls.'))
    hide_categories = models.BooleanField(_('hide categories list'), default=False,
                                          help_text=_('Select if you want to hide the category list view.'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    def clean(self):
        """
        Don't allow articlesmanager to be attached in home page. This cause 404 eror
        :return: cleaned_data and errors
        """
        if self.page.htmlpage.home:
            msg = _("Article manager can't be attached to the home page. Please select another page.")
            raise ValidationError({'page': msg})


class NewsArticleManager(Plugin):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the article news manager.'))
    number = models.IntegerField(_('number'),
                                 help_text=_('Give the number of articles rendering by this manager'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)


class ArticleCategory(models.Model):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the category.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the category, to create the url of the articles which '
                                        'refers to this.'))

    def __unicode__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the article.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the article, to create the url of the article.'))
    body = RichTextField(_('body'))

    category = models.ForeignKey(ArticleCategory, verbose_name=_('category'),
                                 help_text=_('Select the category of this article.'))
    manager = models.ForeignKey(ArticleManager, verbose_name=_('manager'),
                                help_text=_('Select the article manager of this article.'))
    ctime = models.DateTimeField(_('ctime'), auto_now_add=True)

    utime = models.DateTimeField(_('utime'), auto_now=True)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return self.title


