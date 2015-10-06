# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from loosecms.models import Plugin, HtmlPage, LoosecmsTagged
from loosecms.fields import LoosecmsRichTextField, LoosecmsTaggableManager

from parler.models import TranslatableModel, TranslatedFields


class ArticleManager(Plugin):
    default_type = 'ArticleManagerPlugin'

    title = models.CharField(_('title'), max_length=200, unique=True,
                             help_text=_('Give the name of the article manager.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the article manager.'))
    number = models.IntegerField(_('number'), null=True, blank=True,
                                 help_text=_('Give the number of articles per page.'))
    page = models.ForeignKey(HtmlPage, verbose_name=_('page'),
                             limit_choices_to={'is_template': False},
                             help_text=_('Select the page which this article manager will showed. Is needed to know '
                                         'the page of the article manager to create the unique article urls.'))
    category_page = models.BooleanField(_('show category page'), default=True,
                                        help_text=_('Check this box if you want to show all categories in this page'
                                                    'or show instant the articles'))
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
        if self.page.home:
            msg = _("Article manager can't be attached to the home page. Please select another page.")
            raise ValidationError({'page': msg})


class NewsArticleManager(Plugin):
    default_type = 'NewsArticleManagerPlugin'

    title = models.CharField(_('title'), max_length=200, unique=True,
                             help_text=_('Give the name of the article news manager.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the article news manager.'))
    number = models.IntegerField(_('number'),
                                 help_text=_('Give the number of articles rendering by this manager'))
    header_title = models.CharField(_('header title'), max_length=150,
                                    default=_('Recent articles'),
                                    help_text=_('Give the title of the panel which articles will appeared.'))
    rss = models.BooleanField(_('rss'), default=False,
                              help_text=_('Check this box if you want to appear the rss link in the header.'))
    rss_title = models.CharField(_('rss title'), max_length=200, blank=True,
                                 help_text=_('Give the title of the rss feed.'))
    rss_description = models.CharField(_('rss description'), max_length=200, blank=True,
                                       help_text=_('Give a small description for the rss feed.'))
    manager = models.ForeignKey(ArticleManager, verbose_name=_('manager'), blank=True, null=True,
                                limit_choices_to={'published': True},
                                help_text=_('Select the article manager that contain the request articles. In case'
                                            ' of no selection all artilces form all managers will be included.'))
    interval = models.PositiveSmallIntegerField(_('interval'), default=2000,
                                                help_text=_('Set the change rate in miliseconds.'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    def clean(self):
        """
        Don't allow rss title and rss description to be null if rss is checked.
        :return: cleaned_data and errors
        """
        if self.rss:
            if not self.rss_title:
                msg = _('You will need to give a rss title if rss is checked')
                raise ValidationError({'rss_title': msg})
            if not self.rss_description:
                msg = _('You will need to give a rss description if rss is checked')
                raise ValidationError({'rss_description': msg})


class Article(TranslatableModel):
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the article, to create the url of the article.'))
    category = LoosecmsTaggableManager(_('category'), through=LoosecmsTagged)

    manager = models.ForeignKey(ArticleManager, verbose_name=_('manager'),
                                help_text=_('Select the article manager of this article.'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    published = models.BooleanField(_('published'), default=True)

    translations = TranslatedFields(
        title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the article.')),
        body = LoosecmsRichTextField(_('body'))
    )

    def __unicode__(self):
        return self.title

