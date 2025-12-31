from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('post/<slug:slug>/',views.detail,name='detail'),
   path('create/', views.create_post, name='create-post'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit-post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete-post'),




]
