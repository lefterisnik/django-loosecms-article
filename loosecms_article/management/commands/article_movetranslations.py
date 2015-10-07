# -*- coding: utf-8 -*-
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from ...models import Article


class Command(BaseCommand):
    help = 'Move translations from one language to another in case of wrong input'

    def add_arguments(self, parser):
        parser.add_argument('source')
        parser.add_argument('destination')
        parser.add_argument('-pk', '--article-pk', type=int, dest='pk')
        parser.add_argument('-ds', '--delete-source', action='store_true', dest='ds')
        parser.add_argument('-i', '--verbose', action='store_true', dest='verbose')
        parser.add_argument('-ov', '--override', action='store_true', dest='override')

    def handle(self, *args, **options):
        source = options.get('source')
        destination = options.get('destination')
        verbose = options.get('verbose')
        override = options.get('override')
        pk = options.get('pk')
        ds = options.get('ds')

        ArticleTranslation = apps.get_model('loosecms_article', 'ArticleTranslation')

        available_languages = [k for k, v in settings.LANGUAGES]
        if source not in available_languages:
            raise CommandError('Source language not in LANGUAGES: %s' % source)

        if destination not in available_languages:
            raise CommandError('Destination language not in LANGUAGES: %s' % source)

        # If pk is set, then get the article, else fetch all articles
        if pk:
            try:
                articles = Article.objects.get(pk=pk)
                articles = [articles]
            except Article.DoesNotExist:
                raise CommandError('Article "%s" does not exist' % pk)
        else:
            articles = Article.objects.all()

        for article in articles:
            # Fetch the translation of the article for the source language
            source_article = self._get_translation(article, ArticleTranslation, source)

            # If exists, fetch translation of the article for the destination language (if exists set the new values
            # if not exists create an entry and set the values), else throw message
            if source_article:
                destination_article = self._get_translation(article, ArticleTranslation, destination)
                if not destination_article:
                    tmp_title, tmp_body = source_article.title, source_article.body

                    # Because some values are unique we must delete first the source translation
                    source_article.delete()

                    ArticleTranslation.objects.create(
                        master_id=article.pk,
                        language_code=destination,
                        title=tmp_title,
                        body=tmp_body
                    )
                else:
                    if override:
                        destination_article.title = source_article.title
                        destination_article.body = source_article.body
                    else:
                        if not destination_article.title:
                            destination_article.title = source_article.title
                        if not destination_article.body:
                            destination_article.body = source_article.body

                    # Because some values are unique we must delete first the source translation
                    source_article.delete()

                    destination_article.opened = False
                    destination_article.save()

                    if verbose:
                        self.stdout.write('Successfully translation moving "new title: %s"' %
                                      (destination_article.title))
                        self.stdout.write('Successfully translation moving "new body: %s"' %
                                      (destination_article.body))
            else:
                self.stdout.write('The %s article translation does not exist. Will continue to the next article.'
                                  % object.title)

        self.stdout.write('Successfully translation moving.')

    def _get_translation(self, object, ArticleTranslation, language):
        translations = ArticleTranslation.objects.filter(master_id=object.pk)
        try:
            # Try default translation
            return translations.get(language_code=language)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Hope there is a single translation
            return