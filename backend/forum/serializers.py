from rest_framework import serializers
from .models import Post, Tag, Upvote, Comment, CommentLike
from .validators import validate_tags
from drf_writable_nested import WritableNestedModelSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

class CommentsSerializer(serializers.ModelSerializer):

    post_commented=serializers.CharField(source="post_commented.title", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    liked_by = serializers.SerializerMethodField()
    replied_to = serializers.SerializerMethodField()
    # replies = serializers.SerializerMethodField()


    class Meta:
        model = Comment
        fields = ['id', 'user', 'post_commented', 'likes' , 'liked_by' , 'text', 'parent', 'created_at', 'replied_to']

    def get_liked_by(self, obj):
        return [user.username for user in obj.liked_by.all()]
    
    def get_replied_to(self, obj):
        return obj.replied_to
    
    def get_replies(self, obj):
        replies = obj.get_replies()
        serializer = CommentsSerializer(replies, many=True)
        return serializer.data
        
        

class TagSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']

class PostSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):

    author = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, required=True)
    comments = CommentsSerializer(many=True, required=False)
    # liked_by = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_liked_by(self, obj):
        return [user.username for user in obj.liked_by.all()]

class UpvoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Upvote
        fields = ['post', 'user']

class CommentLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ['user','comment']

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

