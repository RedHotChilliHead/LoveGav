from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserPublicDetaislView, CreatePostView, PostDetaislView, PostUpdateView, PostDeleteView, \
    CommentDeleteView, PostListView
from .api_views import PostViewSet, CommentViewSet

routers = DefaultRouter()
routers.register("posts", PostViewSet, basename='post')
routers.register("comments", CommentViewSet, basename='comment')

app_name = "blogapp"

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts-list'),
    path('<str:username>/', UserPublicDetaislView.as_view(), name='public-user-details'),
    path('<str:username>/create_post/', CreatePostView.as_view(), name='create-post'),
    path('<str:username>/post/<int:pk>/', PostDetaislView.as_view(), name='detail-post'),
    path('<str:username>/post/<int:pk>/update', PostUpdateView.as_view(), name='update-post'),
    path('<str:username>/post/<int:pk>/delete', PostDeleteView.as_view(), name='delete-post'),
    path('<str:username>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name="comment-delete"),

    path('api/', include(routers.urls)),
    path('api/posts/<int:pk>/comments/', CommentViewSet.as_view({'get': 'list',
                                                          'post': 'create'})),
    path('api/posts/<int:pk>/comments/<int:comment_pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='comment-detail'),
]
