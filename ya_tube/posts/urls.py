from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path("posts/", views.api_posts, name="posts-list"),
    path("posts/<int:pk>/", views.api_posts_detail, name="posts-detail"),
]
