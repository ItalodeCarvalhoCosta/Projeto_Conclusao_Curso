from django.contrib import admin
from .models import SolicitacaoTreino, Exercicio, FichaTreino, FichaExercicio


@admin.register(SolicitacaoTreino)
class SolicitacaoTreinoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'objetivo_principal', 'nivel_experiencia', 'criado_em')
    search_fields = ('usuario__username', 'objetivo_principal')
    list_filter = ('nivel_experiencia', 'objetivo_principal')


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criado_por', 'criado_em')
    search_fields = ('nome',)


class FichaExercicioInline(admin.TabularInline):
    model = FichaExercicio
    extra = 1


@admin.register(FichaTreino)
class FichaTreinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'objetivo', 'nivel', 'criado_em')
    inlines = (FichaExercicioInline,)