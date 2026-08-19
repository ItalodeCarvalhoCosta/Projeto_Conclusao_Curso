from django.contrib import admin
from .models import PerfilTreino, TreinoPersonalizado, Exercicio


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    """
    Aqui é onde VOCÊ (administrador) cadastra os exercícios da
    biblioteca: nome, imagem, grupo muscular e link do YouTube.
    O usuário comum não tem acesso a essa tela.
    """
    list_display = ('nome', 'grupo_muscular', 'link_youtube')
    list_filter = ('grupo_muscular',)
    search_fields = ('nome',)


@admin.register(PerfilTreino)
class PerfilTreinoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'objetivo', 'nivel_experiencia', 'criado_em')
    list_filter = ('objetivo', 'nivel_experiencia', 'genero')
    search_fields = ('usuario__username',)


@admin.register(TreinoPersonalizado)
class TreinoPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'criado_em')
    readonly_fields = ('conteudo_texto', 'conteudo_json', 'criado_em')