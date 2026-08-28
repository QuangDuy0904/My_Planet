from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('planets/', views.planet, name='planets'),
    path('planets/details/<int:id>/', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
  
]