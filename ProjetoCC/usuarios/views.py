from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from .forms import PerfilForm


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('monitoramento:dashboard')  # ajuste para a rota do monitoramento
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):

    if request.method == 'POST':

        form = PerfilForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            return redirect('monitoramento:dashboard')

    else:

        form = PerfilForm(
            instance=request.user
        )

    return render(
        request,
        'usuarios/perfil.html',
        {
            'form': form
        }
    )