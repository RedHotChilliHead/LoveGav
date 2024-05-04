from django.urls import path

from .views import UserPublicDetaislView, CreatePostView, PostDetaislView, PostUpdateView, PostDeleteView, CommentDeleteView

app_name = "blogapp"

urlpatterns = [
    path('<str:username>/', UserPublicDetaislView.as_view(), name='public-user-details'),
    path('<str:username>/create_post/', CreatePostView.as_view(), name='create-post'),
    path('<str:username>/post/<int:pk>/', PostDetaislView.as_view(), name='detail-post'),
    path('<str:username>/post/<int:pk>/update', PostUpdateView.as_view(), name='update-post'),
    path('<str:username>/post/<int:pk>/delete', PostDeleteView.as_view(), name='delete-post'),
    path('<str:username>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name="comment-delete"),
]
