import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoTreinoForm, FichaTreinoForm
from .models import Exercicio, FichaTreino, FichaExercicio
from .ia import montar_prompt, chamar_ia


@login_required
def criar_treino(request):
    if request.method == 'POST':
        form = SolicitacaoTreinoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()

            try:
                plano = chamar_ia(montar_prompt(solicitacao))
            except (requests.RequestException, json.JSONDecodeError, KeyError):
                return render(request, 'treino/erro_geracao.html', {'solicitacao': solicitacao})

            ficha = FichaTreino.objects.create(
                usuario=request.user,
                nome=plano.get('nome', 'Treino gerado por IA'),
                objetivo=plano.get('objetivo', solicitacao.objetivo_principal),
                nivel=plano.get('nivel', solicitacao.nivel_experiencia),
            )

            for i, ex in enumerate(plano.get('exercicios', []), start=1):
                exercicio_obj, _ = Exercicio.objects.get_or_create(nome=ex['nome'])
                FichaExercicio.objects.create(
                    ficha=ficha, exercicio=exercicio_obj, ordem=i,
                    series=ex.get('series', 3), repeticoes=ex.get('repeticoes', 12),
                )

            solicitacao.ficha_gerada = ficha
            solicitacao.save()
            return redirect('ficha_detail', pk=ficha.pk)
    else:
        form = SolicitacaoTreinoForm()

    return render(request, 'treino/criar_treino.html', {'form': form})


@login_required
def ficha_detail(request, pk):
    ficha = get_object_or_404(FichaTreino, pk=pk, usuario=request.user)
    itens = ficha.fichaexercicio_set.select_related('exercicio').order_by('ordem')
    return render(request, 'treino/ficha_detail.html', {'ficha': ficha, 'itens': itens})


@login_required
def minhas_fichas(request):
    fichas = FichaTreino.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'treino/minhas_fichas.html', {'fichas': fichas})


@login_required
def criar_ficha(request):
    if request.method == 'POST':
        form = FichaTreinoForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.usuario = request.user
            ficha.save()
            exercicios = form.cleaned_data.get('exercicios')
            for ordem, ex in enumerate(exercicios, start=1):
                FichaExercicio.objects.create(ficha=ficha, exercicio=ex, ordem=ordem)
            return redirect('ficha_detail', pk=ficha.pk)
    else:
        form = FichaTreinoForm()

    return render(request, 'treino/criar_ficha.html', {'form': form})


def biblioteca(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'treino/biblioteca.html', {'exercicios': exercicios})


def exercicio_detail(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    return render(request, 'treino/exercicio_detail.html', {'exercicio': exercicio})