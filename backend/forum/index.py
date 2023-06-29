from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Post

@register(Post)
class YourModelIndex(AlgoliaIndex):
    fields = [
        'author',
        'title',
        'body',
        'comment_text',
    ]
    tags = 'tag_names'
    settings = {
        'attributesForFaceting' : ['author']
    }
