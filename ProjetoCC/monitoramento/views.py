from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

from .models import Monitoramento
from .forms import MonitoramentoForm


@login_required
def cadastrar_monitoramento(request):

    hoje = timezone.localdate()

    # Procura se o usuário já registrou dados hoje
    registro_existente = Monitoramento.objects.filter(
        usuario=request.user,
        data=hoje
    ).first()

        # Se já cadastrou hoje, não pode cadastrar novamente
    if registro_existente:
        return redirect('monitoramento:dashboard')

    if request.method == 'POST':

        form = MonitoramentoForm(request.POST)

        if form.is_valid():

            monitoramento = form.save(commit=False)

            monitoramento.usuario = request.user
            monitoramento.data = hoje

            monitoramento.save()

            return redirect('monitoramento:dashboard')

    else:
        form = MonitoramentoForm()

    return render(
        request,
        'monitoramento/cadastrar_monitoramento.html',
        {
            'form': form
        }
    )
    if form.is_valid():

            monitoramento = form.save(commit=False)

            monitoramento.usuario = request.user
            monitoramento.data = hoje

            monitoramento.save()

            return redirect('monitoramento:dashboard')

    else:

        form = MonitoramentoForm(
            instance=registro
        )

    return render(
        request,
        'monitoramento/cadastrar_monitoramento.html',
        {
            'form': form
        }
    )
@login_required
def editar_monitoramento(request):

    hoje = timezone.localdate()

    # Busca o registro de hoje
    registro = Monitoramento.objects.filter(
        usuario=request.user,
        data=hoje
    ).first()

    # Se não existe registro hoje,
    # o usuário precisa cadastrar primeiro
    if not registro:
        return redirect('monitoramento:cadastrar')

    if request.method == 'POST':

        form = MonitoramentoForm(
            request.POST,
            instance=registro
        )

        if form.is_valid():

            form.save()

            return redirect('monitoramento:dashboard')

    else:

        form = MonitoramentoForm(
            instance=registro
        )

    return render(
        request,
        'monitoramento/editar_monitoramento.html',
        {
            'form': form
        }
    )

@login_required
def dashboard(request):

    hoje = timezone.localdate()

    # Busca todos os monitoramentos do usuário logado
    monitoramentos = Monitoramento.objects.filter(
        usuario=request.user
    )

    # Busca o registro feito hoje
    registro_hoje = monitoramentos.filter(
        data=hoje
    ).first()

    # Busca o registro mais recente que possui peso
    ultimo_peso = monitoramentos.filter(
        peso__isnull=False
    ).first()

    # -------------------------
    # PESO ATUAL
    # -------------------------

    if ultimo_peso:
        peso_atual = ultimo_peso.peso
    else:
        peso_atual = None

    # -------------------------
    # IMC
    # -------------------------

    if ultimo_peso:
        imc = ultimo_peso.calcular_imc()
    else:
        imc = None

    # -------------------------
    # ÁGUA DE HOJE
    # -------------------------

    if registro_hoje:
        agua_hoje = registro_hoje.agua
    else:
        agua_hoje = 0

    # -------------------------
    # CARDIO DE HOJE
    # -------------------------

    if registro_hoje:
        tempo_cardio = registro_hoje.tempo_cardio
    else:
        tempo_cardio = 0

    # -------------------------
    # DIAS SEGUINDO A DIETA
    # -------------------------

    dias_dieta = monitoramentos.filter(
        seguiu_dieta=True
    ).count()

    # -------------------------
    # DIAS EM QUE TREINOU
    # -------------------------

    dias_treino = monitoramentos.filter(
        realizou_treino=True
    ).count()

    contexto = {
        'peso_atual': peso_atual,
        'imc': imc,
        'agua_hoje': agua_hoje,
        'tempo_cardio': tempo_cardio,
        'dias_dieta': dias_dieta,
        'dias_treino': dias_treino,
        'registro_hoje': registro_hoje,
    }

    return render(
        request,
        'monitoramento/dashboard.html',
        contexto
    )


@login_required
def dados_peso(request):

    registros = Monitoramento.objects.filter(
        usuario=request.user,
        peso__isnull=False
    ).order_by('data')

    labels = []
    dados = []

    for registro in registros:

        labels.append(
            registro.data.strftime('%d/%m')
        )

        dados.append(
            float(registro.peso)
        )

    return JsonResponse({
        'labels': labels,
        'dados': dados
    })


@login_required
def dados_agua(request):

    registros = Monitoramento.objects.filter(
        usuario=request.user
    ).order_by('data')

    labels = []
    dados = []

    for registro in registros:

        labels.append(
            registro.data.strftime('%d/%m')
        )

        dados.append(
            float(registro.agua)
        )

    return JsonResponse({
        'labels': labels,
        'dados': dados
    })


@login_required
def dados_cardio(request):

    registros = Monitoramento.objects.filter(
        usuario=request.user
    ).order_by('data')

    labels = []
    dados = []

    for registro in registros:

        labels.append(
            registro.data.strftime('%d/%m')
        )

        dados.append(
            registro.tempo_cardio
        )

    return JsonResponse({
        'labels': labels,
        'dados': dados
    })


@login_required
def dados_adesao(request):

    hoje = timezone.localdate()

    registros = Monitoramento.objects.filter(
        usuario=request.user,
        data__year=hoje.year,
        data__month=hoje.month
    ).order_by('data')

    dados = []

    for registro in registros:

        dados.append({
            'dia': registro.data.day,
            'dieta': registro.seguiu_dieta,
            'treino': registro.realizou_treino
        })

    return JsonResponse({
        'ano': hoje.year,
        'mes': hoje.month,
        'registros': dados
    })