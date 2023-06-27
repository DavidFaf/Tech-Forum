from django.db import models
from django.conf import settings
from .validators import validate_tags

User = settings.AUTH_USER_MODEL

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Upvote(models.Model):

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='upvotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_commented = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comments',blank=True, default=None)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
    
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_liked')

    def __str__(self):
        return f"{self.user.username} likes {self.comment.text}"
    
    
class PostView(models.Model):

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
class Post(models.Model):

    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=False, null=False)
    tags = models.ManyToManyField(Tag)
    body = models.TextField(max_length=150, blank=False, null=False)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True ,default=None)
    comments = models.ManyToManyField(Comment, related_name='post_comments', blank=True)
    date_updated = models.DateTimeField(auto_now=True)

    def comment_text(self):
        return [str(comments) for comments in self.comments.all()]

    def tag_names(self):
        return [str(tags) for tags in self.tags.all()]
    
    def __str__(self):
        return self.title


