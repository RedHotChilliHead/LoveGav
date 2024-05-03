from django.urls import path

from .views import UserPublicDetaislView, CreatePostView, PostDetaislView

app_name = "blogapp"

urlpatterns = [
    path('<str:username>/', UserPublicDetaislView.as_view(), name='public-user-details'),
    path('<str:username>/create_post/', CreatePostView.as_view(), name='create-post'),
    path('<str:username>/post/<int:pk>/', PostDetaislView.as_view(), name='detail-post'),
]
