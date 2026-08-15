from django.urls import path
from . import views

app_name = 'monitoramento'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
 path(
        'cadastrar/',
        views.cadastrar_monitoramento,
        name='cadastrar'
    ),

    path(
        'dados/peso/',
        views.dados_peso,
        name='dados_peso'
    ),

    path(
        'dados/agua/',
        views.dados_agua,
        name='dados_agua'
    ),

    path(
        'dados/cardio/',
        views.dados_cardio,
        name='dados_cardio'
    ),

    path(
        'dados/adesao/',
        views.dados_adesao,
        name='dados_adesao'
    ),
    path('editar/', views.editar_monitoramento, name='editar'),

]