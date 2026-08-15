from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]