from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.main, name='main'),
    path('planets/', views.planet, name='planets'),
    path('planets/details/<int:id>/', views.details, name='details'),
    path('testing/', views.testing, name='testing'),



    path('register/', views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('add_blogs/', views.add_blogs, name='add_blog'),
    path('post/<int:id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('chat/', views.user_chat, name='user_chat'),
    path('admin-chat/', views.admin_chat_list, name='admin_chat_list'),
    path('admin-chat/<int:user_id>/', views.admin_chat_detail, name='admin_chat_detail'),
    path('posts/<int:id>/like/', views.like_post, name='like_post'),
  
]