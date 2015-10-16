from django.conf import settings
from django.utils.translation import get_language, activate, deactivate_all
from haystack import indexes
from .models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ctime = indexes.DateTimeField(model_attr='ctime')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """
        Used when the entire index for model is updated.
        """
        return self.get_model().objects.select_related().all()

    def update_object(self, instance, using=None, **kwargs):
        """
        Update the index for a single object. Attached to the class's
        post-save hook.
        """
        instance.set_current_language(settings.LANGUAGE_CODE)
        super(ArticleIndex, self).update_object(instance, using, **kwargs)