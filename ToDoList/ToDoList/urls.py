from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view
from List.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('post/<int:pk>', detail, name='detail'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('author/<str:username>', author, name='author'),
    path('register/', register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='List/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='List/logout.html'), name='logout'),


]
