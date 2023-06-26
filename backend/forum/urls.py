from django.urls import path
from . import views

urlpatterns = [

    # Post urls
    path('posts/', views.PostListCreateApiView.as_view()),
    path('posts/<int:pk>/update/', views.PostUpdateApiView.as_view()),
    path('posts/<int:pk>/delete/', views.PostDestroyApiView.as_view()),
    path('posts/<int:pk>/', views.PostReteiveApiView.as_view()),
    path('posts/<int:pk>/upvote/', views.UpvoteCreateApiView.as_view()),
    path('posts/<int:pk>/liked-by/', views.LikedUsersAPIView.as_view()),

    # Comments urls
    path('comments/', views.CommentListCreateAPiVIew.as_view()),
    path('comments/<int:pk>/', views.CommentRetreiveApiView.as_view()),
    path('comments/<int:pk>/destroy/', views.CommentDestroyApiView.as_view()),
    path('comments/<int:pk>/upvote/', views.LikeCommentApiView.as_view(), name='like-comment'),
    path('comments/<int:pk>/liked-by/', views.CommentLikedBy.as_view()),

    
]



