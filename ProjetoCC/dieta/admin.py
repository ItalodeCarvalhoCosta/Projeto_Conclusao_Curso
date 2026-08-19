from django.contrib import admin
from .models import PerfilDieta, DietaPersonalizada


@admin.register(PerfilDieta)
class PerfilDietaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'objetivo', 'nivel_atividade', 'orcamento_semanal', 'criado_em')
    list_filter = ('objetivo', 'nivel_atividade', 'restricao_alimentar')
    search_fields = ('usuario__username',)


@admin.register(DietaPersonalizada)
class DietaPersonalizadaAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'calorias_alvo', 'proteina_g', 'carboidrato_g', 'gordura_g', 'criado_em')
    readonly_fields = ('conteudo_texto', 'conteudo_json', 'criado_em')