from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_treino, name='criar_treino'),
    path('ficha/criar/', views.criar_ficha, name='criar_ficha'),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    path('exercicio/<int:pk>/', views.exercicio_detail, name='exercicio_detail'),
]