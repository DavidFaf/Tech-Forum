from django.contrib import admin
from .models import *


models = [Tag, Comment, Upvote, PostView, Post, CommentLike]
# Register your models here.
admin.site.register(models)