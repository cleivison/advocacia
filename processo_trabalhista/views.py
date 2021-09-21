from django.shortcuts import render, redirect
from cliente.models import Cliente
from controle_usuario.models import funcionario
from .crawler import add_processo_trab
from .models import Processo_trabalhista, Movimento_trab

def add(request):

    if request.method == 'POST':

        cliente = request.POST.get('clientes')
        if(cliente != ''):
            cliente = Cliente.objects.get(id=cliente)

        advogado = request.POST.get('advogados')
        if(advogado != ''):
            advogado = funcionario.objects.get(id=advogado)

        pr = []
        pr.append(request.POST.get('n_processo'))
        pr.append(request.POST.get('ano_processo'))
        pr.append(request.POST.get('VVV'))
        pr.append(request.POST.get('RR'))
        pr.append(request.POST.get('SS'))

        add_processo_trab(pr,cliente,advogado)

    return redirect('/processos_trabalhista/lista')

def home(request):

    c = Cliente.objects.all()
    users = funcionario.objects.filter(perfil='Advogado')

    return render(request, 'processos_trabalhista.html', {'cliente':c, 'users':users})

def lista(request):

    p = Processo_trabalhista.objects.all()
    m = Movimento_trab.objects.filter()

    return render(request, 'processos_lista.html', {'processo':p, 'movimento':m})