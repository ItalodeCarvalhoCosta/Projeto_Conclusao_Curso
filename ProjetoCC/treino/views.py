from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SolicitacaoTreinoForm

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