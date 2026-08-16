from django.contrib import admin
from .models import PlanoAlimentar, Refeicao


class RefeicaoInline(admin.TabularInline):
    model = Refeicao
    extra = 1


@admin.register(PlanoAlimentar)
class PlanoAlimentarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'calorias_meta', 'criado_em')
    inlines = [RefeicaoInline]


@admin.register(Refeicao)
class RefeicaoAdmin(admin.ModelAdmin):
    list_display = ('plano', 'tipo', 'calorias')