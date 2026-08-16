from django.urls import path
from . import views

app_name = 'dieta'

urlpatterns = [
    path('', views.meu_plano, name='meu_plano'),
    path('criar/', views.criar_plano, name='criar_plano'),
    path('refeicao/nova/', views.criar_refeicao, name='criar_refeicao'),
    path('refeicao/<int:pk>/editar/', views.editar_refeicao, name='editar_refeicao'),
    path('refeicao/<int:pk>/excluir/', views.excluir_refeicao, name='excluir_refeicao'),
]