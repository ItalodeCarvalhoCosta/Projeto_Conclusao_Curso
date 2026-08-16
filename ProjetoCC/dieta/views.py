from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .calculos import calcular_meta_nutricional, DadosIncompletos
from .forms import PlanoAlimentarForm, RefeicaoForm
from .models import PlanoAlimentar, Refeicao


@login_required
def meu_plano(request):
    plano = PlanoAlimentar.objects.filter(usuario=request.user).first()

    if not plano:
        return redirect('dieta:criar_plano')

    refeicoes = plano.refeicoes.all()

    totais = {
        'calorias': sum(r.calorias for r in refeicoes),
        'proteina': sum(r.proteina for r in refeicoes),
        'carboidrato': sum(r.carboidrato for r in refeicoes),
        'gordura': sum(r.gordura for r in refeicoes),
    }

    return render(request, 'dieta/plano.html', {
        'plano': plano,
        'refeicoes': refeicoes,
        'totais': totais,
    })


@login_required
def criar_plano(request):
    ultimo_registro = request.user.monitoramentos.exclude(peso__isnull=True).first()
    peso_atual = ultimo_registro.peso if ultimo_registro else None

    try:
        sugestao = calcular_meta_nutricional(request.user, peso_atual)
        erro = None
    except DadosIncompletos as e:
        sugestao = None
        erro = str(e)

    if request.method == 'POST':
        form = PlanoAlimentarForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.usuario = request.user
            plano.save()
            return redirect('dieta:meu_plano')
    else:
        initial = {}
        if sugestao:
            initial = {
                'calorias_meta': sugestao['calorias'],
                'proteina_meta': sugestao['proteina'],
                'carboidrato_meta': sugestao['carboidrato'],
                'gordura_meta': sugestao['gordura'],
            }
        form = PlanoAlimentarForm(initial=initial)

    return render(request, 'dieta/criar_plano.html', {
        'form': form,
        'sugestao': sugestao,
        'erro': erro,
    })


@login_required
def criar_refeicao(request):
    plano = get_object_or_404(PlanoAlimentar, usuario=request.user)

    if request.method == 'POST':
        form = RefeicaoForm(request.POST)
        if form.is_valid():
            refeicao = form.save(commit=False)
            refeicao.plano = plano
            refeicao.save()
            return redirect('dieta:meu_plano')
    else:
        form = RefeicaoForm()

    return render(request, 'dieta/criar_refeicao.html', {'form': form, 'plano': plano})


@login_required
def editar_refeicao(request, pk):
    refeicao = get_object_or_404(Refeicao, pk=pk, plano__usuario=request.user)

    if request.method == 'POST':
        form = RefeicaoForm(request.POST, instance=refeicao)
        if form.is_valid():
            form.save()
            return redirect('dieta:meu_plano')
    else:
        form = RefeicaoForm(instance=refeicao)

    return render(request, 'dieta/criar_refeicao.html', {'form': form, 'plano': refeicao.plano, 'editando': True})


@login_required
def excluir_refeicao(request, pk):
    refeicao = get_object_or_404(Refeicao, pk=pk, plano__usuario=request.user)

    if request.method == 'POST':
        refeicao.delete()

    return redirect('dieta:meu_plano')