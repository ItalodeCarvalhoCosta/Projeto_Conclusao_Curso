from django.contrib import admin
from .models import Treino, Exercicio, FichaTreino, FichaExercicio


@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_muscular', 'nivel', 'series', 'repeticoes')
    search_fields = ('nome', 'grupo_muscular')
    list_filter = ('nivel', 'grupo_muscular')


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