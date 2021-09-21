from django.shortcuts import render, redirect,get_object_or_404
from .models import Processo, Partes, Movimento, Distribuicao
from cliente.models import Cliente
from .forms import *
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .crawler import *
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from controle_usuario.models import funcionario
import wget
from django.http import JsonResponse
from django.template.loader import render_to_string
import requests
import sys
import codecs
import os, sys
import PyPDF2
import datetime
from django.core import serializers
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='/usuario/login/')
def add(request):

    if request.method == 'POST':

        cliente = request.POST.get('clientes')
        if(cliente != ''):
            cliente = Cliente.objects.get(id=cliente)

        advogado = request.POST.get('advogados')
        if(advogado != ''):
            advogado = funcionario.objects.get(id=advogado)


        add_piaui(request.POST.get('processo', False), cliente, advogado)
        return redirect('/processo/')
        html_form = render_to_string('processos.html',request=request,)
    return JsonResponse({'html_form': html_form})

@login_required(login_url='/usuario/login/')
def processo_lista(request):

    if request.GET.get('descricao'):

        processo_ativo = False
        data_ini = datetime.datetime.strptime(request.GET.get('data_ini'), '%d/%m/%Y').strftime('%Y-%m-%d')
        data_fin = datetime.datetime.strptime(request.GET.get('data_fin'), '%d/%m/%Y').strftime('%Y-%m-%d')

        p = None
        if(request.GET.get('processos') == 'ativo'):

            p = Processo.objects.filter(status_processo=True)

        elif(request.GET.get('processos') == 'inativo'):

            p = Processo.objects.filter(status_processo=False)

        else:
            p = Processo.objects.all()

        if(request.GET.get('pesquisa') == 'numero_processo'):

            processo = p.filter(data_abertura__range=(data_ini, data_fin)).filter(numero_processo__istartswith=request.GET.get('descricao'))

        elif(request.GET.get('pesquisa') == 'natureza'):

            processo = p.filter(data_abertura__range=(data_ini, data_fin)).filter(natureza__istartswith=request.GET.get('descricao'))

        elif(request.GET.get('pesquisa') == 'cliente'):

            processo = p.filter(data_abertura__range=(data_ini, data_fin)).filter(cliente__nome__istartswith=request.GET.get('descricao'))

        elif(request.GET.get('pesquisa') == 'advogado'):

            processo = p.filter(data_abertura__range=(data_ini, data_fin)).filter(usuario__user__first_name__istartswith=request.GET.get('descricao'))

        else:
            processo = Processo.objects.all()

        return HttpResponse(serializers.serialize('json', processo), content_type='application/json')
    else:
        processo = Processo.objects.all().order_by('-id')

    paginator = Paginator(processo, 10)  # mostrar ate 25 por page

    page = request.GET.get('page')
    try:
        processo = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        processo = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        processo = paginator.page(paginator.num_pages)

    users = funcionario.objects.filter(perfil='Advogado')
    cliente = Cliente.objects.all()

    return render(request, 'processos.html', {'processo': processo, 'users' :users, 'cliente': cliente })


@login_required(login_url='/usuario/login/')
def processos_detalhes(request, pk):      

    processo = Processo.objects.get(id=pk)
    partes = Partes.objects.filter(processo=pk)
    distribuicao = Distribuicao.objects.filter(processo=pk)
    movimento = Movimento.objects.filter(processo=pk)
    context = dict (
        processo=processo,
        partes=partes,
        distribuicao=distribuicao,
        movimento=movimento,
    )
    return render(request, 'processos_detalhes.html', context)

@login_required(login_url='/usuario/login/')
def processos_atualizar(request, pk):
    processo = Processo.objects.get(id=pk)
    partes = Partes.objects.filter(processo=pk)
    distribuicao = Distribuicao.objects.filter(processo=pk)
    movimento = Movimento.objects.filter(processo=pk)
    add_piaui_atualiza( processo,movimento)
    context = dict (
        processo=processo,
        partes=partes,
        distribuicao=distribuicao,
        movimento=movimento,
    )
    return render(request, 'processos_detalhes.html', context)


@login_required(login_url='/usuario/login/')
def deletar_processo(request, pk):
    processo = get_object_or_404(Processo,pk=pk)
    data = dict()
    if request.method == 'POST':
        processo.delete()
        data['form_is_valid'] = True
        return redirect('/processo/')
    else:
        context = {'processos': processo}
        data['html_form'] = render_to_string('deletar_processo.html', context, request=request)
    return JsonResponse(data)
