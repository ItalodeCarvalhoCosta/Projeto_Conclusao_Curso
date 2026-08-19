from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import PerfilTreinoForm
from .models import PerfilTreino, TreinoPersonalizado, Exercicio
from .ia import gerar_treino_ia


@login_required
def criar_perfil_treino(request):
    """
    Formulário onde o usuário informa peso, altura, idade, objetivo,
    lesões, etc. Ao salvar, manda direto pra tela que gera o treino.
    """
    if request.method == 'POST':
        form = PerfilTreinoForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            return redirect('treino:gerar_treino', perfil_id=perfil.id)
    else:
        form = PerfilTreinoForm()

    return render(request, 'treino/criar_perfil.html', {'form': form})


@login_required
def gerar_treino(request, perfil_id):
    """
    Pega o PerfilTreino já salvo, manda pra IA (ia.py) e salva o
    resultado em TreinoPersonalizado.
    """
    perfil = get_object_or_404(PerfilTreino, id=perfil_id, usuario=request.user)

    try:
        texto, dados_json = gerar_treino_ia(perfil)
    except Exception:
        messages.error(
            request,
            'Não foi possível gerar o treino agora. Tente novamente em instantes.'
        )
        return redirect('treino:criar_perfil')

    treino = TreinoPersonalizado.objects.create(
        perfil=perfil,
        conteudo_texto=texto,
        conteudo_json=dados_json,
    )
    return redirect('treino:ver_treino', treino_id=treino.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import TreinoPersonalizado


@login_required
def meus_treinos(request):

    treinos = TreinoPersonalizado.objects.filter(
        perfil__usuario=request.user
    ).select_related('perfil')

    return render(
        request,
        'treino/meus_treinos.html',
        {
            'treinos': treinos
        }
    )


@login_required
def ver_treino(request, treino_id):

    treino = get_object_or_404(
        TreinoPersonalizado.objects.select_related('perfil'),
        id=treino_id,
        perfil__usuario=request.user
    )

    return render(
        request,
        'treino/ver_treino.html',
        {
            'treino': treino,
            'dados_treino': treino.conteudo_json
        }
    )


@login_required
def biblioteca_exercicios(request):
    """
    Biblioteca de exercícios: busca por nome (?q=crucifixo).
    Somente leitura pro usuário comum — cadastro/edição/exclusão só
    pelo Django Admin (ver admin.py).
    """
    termo = request.GET.get('q', '').strip()
    exercicios = Exercicio.objects.all()
    if termo:
        exercicios = exercicios.filter(nome__icontains=termo)

    return render(request, 'treino/biblioteca.html', {
        'exercicios': exercicios,
        'termo': termo,
    })