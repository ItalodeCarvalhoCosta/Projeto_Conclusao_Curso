from django.urls import path
from . import views

urlpatterns = [
    path('criar/', views.criar_treino, name='criar_treino'),
    path('ficha/<int:pk>/', views.ficha_detail, name='ficha_detail'),
    path('minhas-fichas/', views.minhas_fichas, name='minhas_fichas'),
    path('ficha/nova/', views.criar_ficha, name='criar_ficha'),
    path('biblioteca/', views.biblioteca, name='biblioteca'),
    path('exercicio/<int:pk>/', views.exercicio_detail, name='exercicio_detail'),
]