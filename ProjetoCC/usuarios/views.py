from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm


def registrar(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('dashboard')  # ajuste para a rota do monitoramento
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})