from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import PerfilDietaForm
from .models import PerfilDieta, DietaPersonalizada
from .ia import gerar_dieta_ia


@login_required
def criar_perfil_dieta(request):
    """Formulário com peso, altura, objetivo, alergias, orçamento, etc."""
    if request.method == 'POST':
        form = PerfilDietaForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            return redirect('dieta:gerar_dieta', perfil_id=perfil.id)
    else:
        form = PerfilDietaForm()

    return render(request, 'dieta/criar_perfil.html', {'form': form})


@login_required
def gerar_dieta(request, perfil_id):
    """
    Calcula as metas nutricionais e chama a IA (ia.py) para montar o
    cardápio; salva tudo em DietaPersonalizada.
    """
    perfil = get_object_or_404(PerfilDieta, id=perfil_id, usuario=request.user)

    try:
        metas, texto, dados_json = gerar_dieta_ia(perfil)
    except Exception:
        messages.error(
            request,
            'Não foi possível gerar a dieta agora. Tente novamente em instantes.'
        )
        return redirect('dieta:criar_perfil')

    dieta = DietaPersonalizada.objects.create(
        perfil=perfil,
        calorias_alvo=metas['calorias_alvo'],
        proteina_g=metas['proteina_g'],
        carboidrato_g=metas['carboidrato_g'],
        gordura_g=metas['gordura_g'],
        conteudo_texto=texto,
        conteudo_json=dados_json,
    )
    return redirect('dieta:ver_dieta', dieta_id=dieta.id)


@login_required
def ver_dieta(request, dieta_id):
    dieta = get_object_or_404(DietaPersonalizada, id=dieta_id, perfil__usuario=request.user)
    return render(request, 'dieta/ver_dieta.html', {'dieta': dieta})


@login_required
def minhas_dietas(request):
    dietas = DietaPersonalizada.objects.filter(perfil__usuario=request.user)
    return render(request, 'dieta/minhas_dietas.html', {'dietas': dietas})