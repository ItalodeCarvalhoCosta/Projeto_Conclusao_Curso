from django.urls import path
from . import views

app_name = 'treino'

urlpatterns = [
    path('perfil/novo/', views.criar_perfil_treino, name='criar_perfil'),
    path('perfil/<int:perfil_id>/gerar/', views.gerar_treino, name='gerar_treino'),
    path('treino/<int:treino_id>/', views.ver_treino, name='ver_treino'),
    path('meus-treinos/', views.meus_treinos, name='meus_treinos'),
    path('biblioteca/', views.biblioteca_exercicios, name='biblioteca'),
]