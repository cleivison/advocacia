# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect,get_object_or_404
from .models import Evento
from cliente.models import Cliente
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import EventoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import datetime
from django.core import serializers
from django.http import HttpResponse
import json

@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.agenda', login_url='/usuario/error/')
def home(request):

    if request.GET.get('descricao'):

        data_ini = datetime.datetime.strptime(request.GET.get('data_ini'), '%d/%m/%Y').strftime('%Y-%m-%d')
        data_fin = datetime.datetime.strptime(request.GET.get('data_fin'), '%d/%m/%Y').strftime('%Y-%m-%d')
        if(request.GET.get('pesquisa') == 'funcionario'):

            eventos = Evento.objects.filter(data__range=(data_ini, data_fin)).filter(usuario__user__first_name__istartswith=request.GET.get('descricao'))

        elif(request.GET.get('pesquisa') == 'cliente'):

            eventos = Evento.objects.filter(data__range=(data_ini, data_fin)).filter(cliente__nome__istartswith=request.GET.get('descricao'))

        return HttpResponse(serializers.serialize('json', eventos), content_type='application/json')
    else:
        eventos= Evento.objects.all()

    paginator = Paginator(eventos, 10)  # mostrar ate 25 eventos por page

    page = request.GET.get('page')
    try:
        eventos= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        eventos= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        eventos= paginator.page(paginator.num_pages)

    return render(request, 'home_agenda.html', {'eventos': eventos})


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.agenda', login_url='/usuario/error/')
def detalhes(request, pk):

    evento = Evento.objects.get(id_evento=pk)

    context = dict(
        ev=evento
    )
    return render(request, 'detalhe_eventos.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.agenda', login_url='/usuario/error/')
def deletar(request, pk):
    evento = get_object_or_404(Evento,id_evento=pk)
    data = dict()
    if request.method == 'POST':
        evento.delete()
        data['form_is_valid'] = True
        return redirect('/agenda/')
    else:
        context = {'evento': evento}
        data['html_form'] = render_to_string('modal.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.agenda', login_url='/usuario/error/')
def novo_evento(request):

    context = dict(

        form_ev=EventoForm()
    )

    if request.POST:
        form = EventoForm(request.POST)

        if not form.is_valid():
            return render(request, 'novo_evento.html', dict(form_ev=form))

        form.save()
        return redirect('/agenda/')
    return render(request, 'novo_evento.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.agenda', login_url='/usuario/error/')
def atualizar_contato(request, pk):
    evento = Evento.objects.get(id_evento=pk)

    context = dict(
        form_ev=EventoForm(instance=evento)
    )

    if request.POST:
        form = EventoForm(request.POST, instance=evento)

        if not form.is_valid():
            return render(
                request, 'atualizar_evento.html', dict(
                    form_ev=form
                )
            )

        form.save()
        return redirect('/agenda/')
    return render(request, 'atualizar_evento.html', context)
