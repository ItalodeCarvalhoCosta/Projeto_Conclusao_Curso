from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoTreinoForm
from .forms import FichaTreinoForm
from .models import Exercicio, FichaTreino, FichaExercicio
from django.shortcuts import get_object_or_404

@login_required
def criar_treino(request):
    if request.method == 'POST':
        form = SolicitacaoTreinoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.usuario = request.user
            solicitacao.save()
            # por enquanto, sem IA, só redireciona
            return redirect('treino_sucesso')  # crie essa view/rota se quiser uma msg de confirmação
    else:
        form = SolicitacaoTreinoForm()

    # aqui você pega o perfil do usuário (ajuste ao nome real do seu model)
    perfil = request.user.perfil  # ex: se usuarios/models.py tem OneToOneField com related_name='perfil'

    return render(request, 'treino/criar_treino.html', {
        'form': form,
        'perfil': perfil,
    })



@login_required
def criar_ficha(request):
    if request.method == 'POST':
        form = FichaTreinoForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.usuario = request.user
            ficha.save()
            exercicios = form.cleaned_data.get('exercicios')
            ordem = 1
            for ex in exercicios:
                FichaExercicio.objects.create(
                    ficha=ficha,
                    exercicio=ex,
                    ordem=ordem,
                )
                ordem += 1

            return redirect('perfil')
    else:
        form = FichaTreinoForm()

    return render(request, 'treino/criar_ficha.html', {'form': form})


def biblioteca(request):
    exercicios = Exercicio.objects.all()
    return render(request, 'treino/biblioteca.html', {'exercicios': exercicios})


def exercicio_detail(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk)
    return render(request, 'treino/exercicio_detail.html', {'exercicio': exercicio})