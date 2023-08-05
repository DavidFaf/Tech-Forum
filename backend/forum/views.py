
from rest_framework import generics, status
from .models import Post, PostView, Upvote , Comment, CommentLike
from .serializers import (
    PostSerializer ,
    UpvoteSerializer, 
    CommentsSerializer,
    CommentLikeSerializer,
    UserDetailSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    )
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
User = get_user_model()

class PostListCreateApiView(generics.ListCreateAPIView):

    queryset = Post.objects.all().order_by('-likes')
    serializer_class = PostSerializer

    def perfrom_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

class PostUpdateApiView(generics.UpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDestroyApiView(generics.DestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostReteiveApiView(generics.RetrieveAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user_viewed = False
        if request.user.is_authenticated:
            user_viewed = PostView.objects.filter(post=instance, user=request.user).exists()

        if not user_viewed:
            instance.views += 1
            instance.save()

            if request.user.is_authenticated:
                PostView.objects.create(post=instance, user=request.user)

        return super().retrieve(request, *args, **kwargs)
    
class UpvoteCreateApiView(generics.UpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = UpvoteSerializer

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        id = self.kwargs.get('id')

        if Upvote.objects.filter(post=post, user=self.request.user).exists():
            return Response({"message":"You have liked this post before"}, status=status.HTTP_200_OK)

        post.likes += 1 
        post.liked_by.add(self.request.user)
        post.save()

        Upvote.objects.create(post=post, user=self.request.user)
     

        return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
    
class UpvoteDestroyApiView(generics.UpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = UpvoteSerializer

    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        post = self.get_object()
        id = self.kwargs.get('id')

        # if Upvote.objects.filter(post=post, user=self.request.user).exists():
        #     return Response({"message":"You have liked this post before"})

        if post.likes >=0:
            post.likes -= 1 
            post.liked_by.remove(self.request.user)
            post.save()

        # Upvote.objects.create(post=post, user=self.request.user)
     

        return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
    

class LikeCommentApiView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentLikeSerializer

    def patch(self, *args, **kwargs):
        comment = self.get_object()
        user = self.request.user

        if CommentLike.objects.filter(user=user, comment=comment).exists():
            return Response({"message" : "You have liked this post before"})

        comment.likes += 1
        comment.liked_by.add(user)
        comment.save()

        CommentLike.objects.create(user=user, comment=comment)

        return Response({'message': 'Comment liked successfully.'}, status=status.HTTP_200_OK)

class CommentListCreateAPiVIew(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-likes')
    serializer_class = CommentsSerializer



class CommentRetreiveApiView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


class CommentDestroyApiView(generics.DestroyAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    
class CommentLikedBy(generics.ListAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
            pk = self.kwargs.get('pk')
            queryset = Comment.objects.filter(pk=pk)
            
            if queryset.exists():
                comment = queryset.first()
                return comment.liked_by.all()
            return Response({"message":"Comment doesn't exist"})

    
class LikedUsersAPIView(generics.ListAPIView):
    serializer_class = UserDetailSerializer

    def get_queryset(self):
            pk = self.kwargs.get('pk')
            queryset = Post.objects.filter(pk=pk)
            
            if queryset.exists():
                post = queryset.first()
                return post.liked_by.all()
            return Response({"message":"Post doesn't exist"})


class CreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    

class ChangePasswordView(APIView):
    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            confirm_password = serializer.validated_data.get('confirm_password')

            if not user.check_password(old_password):
                return Response({"message": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"message": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)