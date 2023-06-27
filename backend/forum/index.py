from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Post

@register(Post)
class YourModelIndex(AlgoliaIndex):
    fields = [
        'author',
        'title',
        'tag_names',
        'body',
        'comment_text',
    ]
