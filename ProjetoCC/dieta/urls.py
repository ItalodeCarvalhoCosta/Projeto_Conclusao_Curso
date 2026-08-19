from django.urls import path
from . import views

app_name = 'dieta'

urlpatterns = [
    path('perfil/novo/', views.criar_perfil_dieta, name='criar_perfil'),
    path('perfil/<int:perfil_id>/gerar/', views.gerar_dieta, name='gerar_dieta'),
    path('dieta/<int:dieta_id>/', views.ver_dieta, name='ver_dieta'),
    path('minhas-dietas/', views.minhas_dietas, name='minhas_dietas'),
]