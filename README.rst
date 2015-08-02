=======================
Django Loose CMS - Text
=======================

An article plugin for Django Loose CMS with WYSWYG embeded editor for the article's body.

Requirements
------------

Loose CMS Text plugin requires:

* Django version 1.8
* Python 2.6 or 2.7
* django-loose-cms
* django-ckeditor
* django-haystack

Quick Start
-----------

1. Instalation via pip::

    pip install https://github.com/lefterisnik/django-loosecms-article/archive/master.zip

2. Add "loosecms_article" to your INSTALLED_APPS setting after "loosecms" like this::

    INSTALLED_APPS = (
        ...
        'loosecms_article',
    )

3. Add "django.contrib.humanize" to your INSTALLED_APPS setting after "django.contrib.staticfiles" and before "loosecms"
   like this::

    INSTALLED_APPS = (
        ...
        'django.contrib.humanize',
    )

4. Run ``python manage.py migrate`` to create the loosecms_text models.

5. Run development server ``python manage.py runserver`` and visit http://127.0.0.1:8000/ to start
   playing with the cms.