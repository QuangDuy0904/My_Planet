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
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('add_blogs/', views.add_blogs, name='add_blog'),
  
]