from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_treino, name='criar_treino'),
]