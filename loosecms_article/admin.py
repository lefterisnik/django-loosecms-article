# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from .models import *
from .plugin import *


class ArticleCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'utime'
    list_display = ('title', 'manager', 'get_page', 'published')
    list_filter = ('manager__page', 'manager')
    
    def get_page(self, obj):
        return obj.manager.page
    get_page.short_description = _('Page')
    get_page.admin_order_field = 'manager__page'

admin.site.register(ArticleManager, ArticlePlugin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(NewsArticleManager, NewsArticlePlugin)
admin.site.register(Article, ArticleAdmin)