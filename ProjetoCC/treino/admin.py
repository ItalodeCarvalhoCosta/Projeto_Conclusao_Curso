from django.contrib import admin
from .models import Treino

@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'grupo_muscular', 'nivel', 'series', 'repeticoes')
    search_fields = ('nome', 'grupo_muscular')
    list_filter = ('nivel', 'grupo_muscular')