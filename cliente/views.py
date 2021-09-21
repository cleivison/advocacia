from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from .models import Cliente, Trabalhista
from .forms import *
from django.core import serializers
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
import datetime


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.cadastro', login_url='/usuario/error/')
def listar(request):

    if request.GET.get('pesquisa'):

        if(request.GET.get('pesquisa') == 'qtd_processo'):
            clientes = Cliente.objects.filter(processo__isnull=False).annotate(itemcount=Count('id')).order_by('-itemcount')

        elif(request.GET.get('pesquisa') == 'agendamento'):
            data_ini = datetime.datetime.strptime(request.GET.get('data_ini'), '%d/%m/%Y').strftime('%Y-%m-%d')
            data_fin = datetime.datetime.strptime(request.GET.get('data_fin'), '%d/%m/%Y').strftime('%Y-%m-%d')
            clientes = Cliente.objects.filter(evento__isnull=False).filter(evento__data__range=(data_ini, data_fin))

        elif(request.GET.get('pesquisa') == 'sexo'):
            clientes = Cliente.objects.filter(sexo=request.GET.get('sexo'))
        else:
            clientes = Cliente.objects.all()

        print(serializers.serialize('json', clientes))
        return HttpResponse(serializers.serialize('json', clientes), content_type='application/json')
    else:
        clientes = Cliente.objects.all()

    paginator = Paginator(clientes, 10)  # mostrar ate 25 clientes por page

    page = request.GET.get('page')
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clientes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clientes = paginator.page(paginator.num_pages)

    return render(request, 'cadastro.html', {'clientes': clientes})

# adicionar e editar
@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.cadastro', login_url='/usuario/error/')
def add(request, pk=None):
    if pk is None:
        c = Cliente()
    else:
        c = Cliente.objects.get(pk=pk)

    if request.method == 'POST':
        cliente = ClienteForm(request.POST or None, request.FILES, instance=c,prefix="main")
        trabalhista = TrabalhistaInline(request.POST, request.FILES, instance=c)
        documento=docI(request.POST, request.FILES,instance=c,prefix="product")
        if cliente.is_valid()  and documento.is_valid() and trabalhista.is_valid():
            cliente.save()
            documento.save()
            trabalhista.save()
            return redirect('/cliente/')
    else:
        cliente = ClienteForm(instance=c,prefix="main")
        trabalhista = TrabalhistaInline(instance=c)
        documento = docI(instance=c,prefix="product")

    context = dict({
        'cliente': cliente,
        'form': documento,
        'trabalhista': trabalhista,
    })

    return render(request, 'add.html', context)


# sim ele esta deletando em cascata
@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.cadastro', login_url='/usuario/error/')
def deletar(request,pk):
    cliente = get_object_or_404(Cliente,pk=pk)
    data = dict()
    if request.method == 'POST':
        cliente.delete()
        data['form_is_valid'] = True
        return redirect('/cliente/')
    else:
        context = {'cliente': cliente}
        data['html_form'] = render_to_string('lista.html', context, request=request)
    return JsonResponse(data)




@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.cadastro', login_url='/usuario/error/')
def detalhes(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    trabalhista = Trabalhista.objects.filter(pk=cliente.id)
    context = dict({
        'cliente': cliente,  'trabalhista': trabalhista
    })
    return render(request, 'detalhes.html', context)

def lista(request):
    if request.GET.get('busca'):
        clientes = Cliente.objects.filter(nome__contains=request.GET.get('busca'))
        print(clientes)
        return HttpResponse(serializers.serialize('json', clientes), content_type='application/json')
    else:
        return render(request, 'lista.html', {'clientes': None})
"""
def view_pdf(request, pk):
    pdf = get_object_or_404(Documentos, pk=pk)
    image_data = open(pdf.doc.url, "rb").read()
    return HttpResponse(image_data, contenttype='application/pdf')
"""