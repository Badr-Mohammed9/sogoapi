from django.contrib import admin
from django.urls import path 
from . import views
from .views import *
urlpatterns = [
    path('',views.get_all_groups),
    path("create/", views.create_group),
    path('image/<str:filename>/', views.image_file_view, name='image_file_view'),
    path('image/posts/<str:filename>/', views.image_file_view_posts, name='image_file_view'),
    path('<str:pk>',views.get_group),
    path('post/create/', PostViewSet.as_view({'post': 'create'}), name='create_post'),
    path('<int:group_id>/posts/', get_posts_by_group, name='get_posts_by_group'),
    path('posts/<int:post_id>/', views.delete_post, name='delete_post'),
    path('<int:group_id>/add-participant/', views.add_participant, name='add_participant'),
    path('owner/<int:owner_id>/',views.get_owner_groups),
    path('topic/<str:topic>/', get_groups_by_topic, name='get_groups_by_topic'),
]