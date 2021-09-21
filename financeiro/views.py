# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from .models import Conta_pagar
from .models import Conta_receber
from .models import Parcela
from .models import Conta
from .forms import *
from processos.models import Processo
from django.shortcuts import redirect
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse as response
from django.core import serializers
from django.http import JsonResponse
import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
import datetime
import json
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist


def converterValor(valor):
    valor = valor[3:]
    valor = valor.replace('.', '')
    valor = valor.replace(',', '.')
    return float(valor)
def converterV(valor):
    valor = valor[2:]
    valor = valor.replace('.', '')
    valor = valor.replace(',', '.')
    return float(valor)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def contaPagar(request):

    if request.method == "POST":
        form = Conta_pagarForm(request.POST)
        if form.is_valid():
            conta_pagar = form.save()
            # converter para númerico

            if (conta_pagar.forma_pagamento == 'Cartão de credito' or conta_pagar.forma_pagamento == 'Cheque'):
                v_total = converterValor(conta_pagar.valor_total)
                v_entrada = converterValor(conta_pagar.valor_entrada)
                v_total = v_total - v_entrada
                conta_pagar.valor_total = str('R$ ') + str(v_total) + str('0')
                conta_pagar.valor_parcela = v_total / conta_pagar.n_parcela
                conta_pagar.save()

                for i in range(conta_pagar.n_parcela):
                    parcela = Parcela()
                    parcela.conta_id = conta_pagar.id
                    parcela.vencimento = conta_pagar.vencimento
                    parcela.save()
                    conta_pagar.vencimento = conta_pagar.vencimento + relativedelta(months=1)
            else:
                conta_pagar.n_parcela = 0
                conta_pagar.valor_entrada = 0
                conta_pagar.valor_parcela = 0
                conta_pagar.save()

            return redirect("/contas/pagar/")
    else:
        form = Conta_pagarForm()
    return render(request, 'a_pagar/contas_pagar_add.html', {'form': form})


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def contaReceber(request, pk = None):

    if request.method == "POST":
        form = Conta_receberForm(request.POST)
        if form.is_valid():
            conta_receber = form.save()
            # converter dados para numerico
            if pk != None:
                p = Processo.objects.get(pk=pk)
                conta_receber.processo = p

            if (conta_receber.forma_pagamento == 'Cartão de credito' or conta_receber.forma_pagamento == 'Cheque'):
                v_total = converterValor(conta_receber.valor_total)
                v_entrada = converterValor(conta_receber.valor_entrada)
                v_total = v_total - v_entrada
                conta_receber.valor_total = str('R$ ') + str(v_total) + str('0')
                conta_receber.valor_parcela = v_total / conta_receber.n_parcela
                conta_receber.save()

                for i in range(conta_receber.n_parcela):
                    parcela = Parcela()
                    parcela.conta_id = conta_receber.id
                    parcela.vencimento = conta_receber.vencimento
                    parcela.save()
                    conta_receber.vencimento = conta_receber.vencimento + relativedelta(months=1)
            else:
                conta_receber.n_parcela = 0
                conta_receber.valor_entrada = 0
                conta_receber.valor_parcela = 0
                conta_receber.save()

            return redirect("/contas/receber/")
    else:
        form = Conta_receberForm()
        if pk != None:
            try:
                c = Conta_receber.objects.get(processo_id = pk)
                return redirect("/contas/receber/"+str(c.id)+"/")
            except ObjectDoesNotExist:
                print('objeto nao existe')

            p = Processo.objects.get(pk=pk)            
            form.initial['descricao'] = p.cliente.nome +' || '+p.numero_processo
            form.initial['observacao'] = 'Cliente:' + p.cliente.nome +'\n' +'N° Processo:'+ p.numero_processo+'\n'
            form.initial['observacao'] += 'Data do processo:'+ p.data_abertura.strftime('%Y-%m-%d %H:%M') +'\n'+ 'Advogado:' +p.usuario.user.first_name+''+ p.usuario.user.last_name
        return render(request, 'a_receber/contas_receber_add.html', {'form': form})

"""
@login_required(login_url='/usuario/login/')
def contas(request):
    contas = Conta_pagar.objects.all()
    data = serializers.serialize('json', contas)
    return HttpResponse(data)

"""


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def contas_pagar_lista(request):

    if request.is_ajax():
        a = Conta_pagar.objects.filter(id=0)
        b = Conta_pagar.objects.filter(id=0)

        contas = Conta_pagar.objects.all()
        if(request.GET.get('aberta') == 's'):
            a = contas.filter(status_pag=False)

        if(request.GET.get('paga') == 's'):
            a = contas.filter(status_pag=True)

        if(request.GET.get('fixas') == 's'):
            b = contas.filter(conta_fixa=True)

        conta = list(Conta.objects.filter(id__in=a | b))
        conta_p = list(a | b)
        z = dict()
        aux = []

        for i in range(0, len(conta)):
            aux.append([conta[i], conta_p[i]])

        for i in range(0, len(conta)):
            z.update({i: serializers.serialize('json', aux[i])})

        return HttpResponse(json.dumps(z, ensure_ascii=True), content_type='application/json')
    else:
        contas = Conta_pagar.objects.all()

    return render(request, 'a_pagar/contas_pagar.html', {'contas': contas})


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def contas_receber_lista(request):

    if request.is_ajax():
        a = Conta_receber.objects.filter(id=0)
        b = Conta_receber.objects.filter(id=0)

        contas = Conta_receber.objects.all()
        if(request.GET.get('aberta') == 's'):
            a = contas.filter(status_pag=False)

        if(request.GET.get('paga') == 's'):
            a = contas.filter(status_pag=True)

        if(request.GET.get('fixas') == 's'):
            b = contas.filter(conta_fixa=True)

        conta = list(Conta.objects.filter(id__in=a | b))
        conta_p = list(a | b)
        z = dict()
        aux = []

        for i in range(0, len(conta)):
            aux.append([conta[i], conta_p[i]])

        for i in range(0, len(conta)):
            z.update({i: serializers.serialize('json', aux[i])})

        return HttpResponse(json.dumps(z, ensure_ascii=True), content_type='application/json')
    else:
        contas = Conta_receber.objects.all()

    return render(request, 'a_receber/contas_receber.html', {'contas': contas})


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def conta_detalhada_pagar(request, pk):

    conta = Conta_pagar.objects.get(id=pk)
    parcela = Parcela.objects.filter(conta_id=conta.id)

    context = dict(
        conta=conta,
        parcela=parcela
    )

    return render(request, 'a_pagar/conta_detalhada_pagar.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def conta_detalhada_receber(request, pk):
    conta = Conta_receber.objects.get(id=pk)
    parcela = Parcela.objects.filter(pk=conta.pk)

    context = dict(
        conta=conta,
        parcela=parcela,
    )
    return render(request, 'a_receber/conta_detalhada_receber.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def deletar_pagar(request, pk):
    conta = get_object_or_404(Conta_pagar,pk=pk)
    data = dict()
    if request.method == 'POST':
        conta.delete()
        data['form_is_valid'] = True
        return redirect('/contas/pagar/')
    else:
        context = {'conta': conta}
        data['html_form'] = render_to_string('modal_delete.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def deletar_receber(request, pk):
    conta = get_object_or_404(Conta_receber,pk=pk)
    data = dict()
    if request.method == 'POST':
        conta.delete()
        data['form_is_valid'] = True
        return redirect('/contas/receber/')
    else:
        context = {'c': conta}
        data['html_form'] = render_to_string('a_receber/deletar.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def atualizar_conta_pagar(request, pk):
    conta = Conta_pagar.objects.get(id=pk)

    context = dict(
        form=Conta_pagarForm(instance=conta)
    )

    if request.POST:
        form = Conta_pagarForm(request.POST, instance=conta)

        if not form.is_valid():
            return render(
                request, 'a_pagar/contas_pagar_add.html', dict(
                    form=form
                )
            )

        conta = form.save()

        Parcela.objects.filter(conta=pk).delete()

        if (conta.forma_pagamento == 'Cartão de credito' or conta.forma_pagamento == 'Cheque'):

            v_total = converterValor(conta.valor_total)
            conta.valor_parcela = v_total / conta.n_parcela
            conta.save()
            for i in range(conta.n_parcela):
                    form_parcela = Parcela()
                    form_parcela.conta_id = conta.id
                    form_parcela.vencimento = conta.vencimento
                    form_parcela.save()
                    conta.vencimento = conta.vencimento + relativedelta(months=1)
        else:
                conta.n_parcela = 0
                conta.valor_entrada = 0
                conta.valor_parcela = 0
                conta.save()

        return redirect("/contas/pagar/")

    return render(request, 'a_pagar/contas_pagar_add.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def atualizar_conta_receber(request, pk):
    conta = Conta_receber.objects.get(id=pk)

    context = dict(
        form=Conta_receberForm(instance=conta)
    )

    if request.POST:
        form = Conta_receberForm(request.POST, instance=conta)

        if not form.is_valid():
            return render(
                request, 'a_receber/contas_receber_add.html', dict(
                    form=form
                )
            )

        conta = form.save()

        Parcela.objects.filter(conta=pk).delete()

        if (conta.forma_pagamento == 'Cartão de credito' or conta.forma_pagamento == 'Cheque'):

            v_total = converterValor(conta.valor_total)
            conta.valor_parcela = v_total / conta.n_parcela
            conta.save()
            for i in range(conta.n_parcela):
                    form_parcela = Parcela()
                    form_parcela.conta_id = conta.id
                    form_parcela.vencimento = conta.vencimento
                    form_parcela.save()
                    conta.vencimento = conta.vencimento + relativedelta(months=1)
        else:
                conta.n_parcela = 0
                conta.valor_entrada = 0
                conta.valor_parcela = 0
                conta.save()

        return redirect("/contas/receber")
    return render(request, 'a_receber/contas_receber_add.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
#filtro de contas a pagar nao pagas
def conta_pagar_aberta(request):
    contas = Conta_pagar.objects.filter(status_pag=False)
    context = dict(
        contas=contas
    )
    return render(request, 'a_pagar/contas_pagar_aberta.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
#filtro de contas a pagar pagas
def conta_apagar_pagas(request):
    contas = Conta_pagar.objects.filter(status_pag=True)
    context = dict(
        contas=contas
    )
    return render(request, 'a_pagar/contas_apagar_concluidas.html', context)

@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
#filtro de contas fixas
def contas_fixas(request):
    contas = Conta_pagar.objects.filter(conta_fixa=True)
    context = dict(
        contas=contas
    )
    return render(request, 'a_pagar/contas_fixas.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
#filtro de contas a receber nao pagas
def conta_receber_aberta(request):
    contas = Conta_receber.objects.filter(status_pag=False)
    context = dict(
        contas=contas
    )
    return render(request, 'a_receber/contas_receber_aberta.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
#filtro de contas a receber pagas
def conta_receber_pagas(request):
    contas = Conta_receber.objects.filter(status_pag=True)
    context = dict(
        contas=contas
    )
    return render(request, 'a_receber/contas_receber_concluidas.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def pagar_parcela(request, pk):

    parcela = Parcela.objects.get(id=pk)

    if (parcela.status_pag != True):
        parcela.data_pag = timezone.now()
        parcela.status_pag = True
        parcela.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#adiciona mais  opcoes de categorias de  conta fixa
@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.financeiro', login_url='/usuario/error/')
def add_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/contas/add_pagar')
    return render(request,'a_pagar/contas_pagar_add.html',{'categoria':form})
def receitas(request):
    #contas a pagar 
    janeiro   = Conta_pagar.objects.filter(vencimento__month=1)
    fevereiro = Conta_pagar.objects.filter(vencimento__month=2)
    marco     = Conta_pagar.objects.filter(vencimento__month=3)
    abril     = Conta_pagar.objects.filter(vencimento__month=4)
    maio      = Conta_pagar.objects.filter(vencimento__month=5)
    junho     = Conta_pagar.objects.filter(vencimento__month=6)
    julho     = Conta_pagar.objects.filter(vencimento__month=7)
    agosto    = Conta_pagar.objects.filter(vencimento__month=8)
    setembro  = Conta_pagar.objects.filter(vencimento__month=9)
    outubro   = Conta_pagar.objects.filter(vencimento__month=10)
    novembro  = Conta_pagar.objects.filter(vencimento__month=11)
    dezembro  = Conta_pagar.objects.filter(vencimento__month=12)
    #queryset1 = Conta_receber.objects.all()
    #saldo = queryset - queryset1
    #names = [str(obj.vencimento) for obj in janeiro]
    #######################################################
    janeiro   = [converterV(obj.valor_total) for obj in janeiro]
    fevereiro = [converterV(obj.valor_total) for obj in fevereiro]
    marco     = [converterV(obj.valor_total) for obj in marco]
    abril     = [converterV(obj.valor_total) for obj in abril]
    maio      = [converterV(obj.valor_total) for obj in maio]
    junho     = [converterV(obj.valor_total) for obj in junho]
    julho     = [converterV(obj.valor_total) for obj in julho]
    agosto    = [converterV(obj.valor_total) for obj in agosto]
    setembro  = [converterV(obj.valor_total) for obj in setembro]
    novembro  = [converterV(obj.valor_total) for obj in novembro]
    dezembro  = [converterV(obj.valor_total) for obj in dezembro]

    #contas a receber
    rec_janeiro   = Conta_receber.objects.filter(vencimento__month=1)
    rec_fevereiro = Conta_receber.objects.filter(vencimento__month=2)
    rec_marco     = Conta_receber.objects.filter(vencimento__month=3)
    rec_abril     = Conta_receber.objects.filter(vencimento__month=4)
    rec_maio      = Conta_receber.objects.filter(vencimento__month=5)
    rec_junho     = Conta_receber.objects.filter(vencimento__month=6)
    rec_julho     = Conta_receber.objects.filter(vencimento__month=7)
    rec_agosto    = Conta_receber.objects.filter(vencimento__month=8)
    rec_setembro  = Conta_receber.objects.filter(vencimento__month=9)
    rec_outubro   = Conta_receber.objects.filter(vencimento__month=10)
    rec_novembro  = Conta_receber.objects.filter(vencimento__month=11)
    rec_dezembro  = Conta_receber.objects.filter(vencimento__month=12)
    
    #contas a receber
    #######################################################
    receber_janeiro   = [converterV(obj.valor_total) for obj in rec_janeiro]
    receber_fevereiro = [converterV(obj.valor_total) for obj in rec_fevereiro]
    receber_marco     = [converterV(obj.valor_total) for obj in rec_marco]
    receber_abril     = [converterV(obj.valor_total) for obj in rec_abril]
    receber_maio      = [converterV(obj.valor_total) for obj in rec_maio]
    receber_junho     = [converterV(obj.valor_total) for obj in rec_junho]
    receber_julho     = [converterV(obj.valor_total) for obj in rec_julho]
    receber_agosto    = [converterV(obj.valor_total) for obj in rec_agosto]
    receber_setembro  = [converterV(obj.valor_total) for obj in rec_setembro]
    receber_outubro   = [converterV(obj.valor_total) for obj in rec_outubro]
    receber_novembro  = [converterV(obj.valor_total) for obj in rec_novembro]
    receber_dezembro  = [converterV(obj.valor_total) for obj in rec_dezembro]
    #saldo

    jan = sum(receber_janeiro)-sum(janeiro)
    fev = sum(receber_fevereiro)-sum(fevereiro)
    mar = sum(receber_marco)- sum(marco)
    abr = sum(receber_abril)- sum(abril)
    mai = sum(receber_maio)- sum(maio)
    jun = sum(receber_junho)- sum(junho)
    jul = sum(receber_julho)- sum(julho)
    ago = sum(receber_agosto)-sum(agosto)
    setb= sum(receber_setembro) - sum(setembro)
    out = sum(receber_outubro)-sum (outubro)
    nov = sum(receber_novembro)-sum (novembro)
    dez = sum(receber_dezembro)- sum(dezembro)


    context = {
        #contas_a pagar
        'janeiro': json.dumps(sum(janeiro)),
        'fevereiro':json.dumps(sum(fevereiro)),
        'marco':json.dumps(sum(marco)),
        'abril':json.dumps(sum(abril)),
        'maio':json.dumps(sum(maio)),
        'junho':json.dumps(sum(junho)),
        'julho':json.dumps(sum(julho)),
        'agosto':json.dumps(sum(agosto)),
        'setembro':json.dumps(sum(setembro)),
        'outubro':json.dumps(sum(outubro)),
        'novembro':json.dumps(sum(novembro)),
        'dezembro':json.dumps(sum(dezembro)),
        #contas_a receber
        'receber_janeiro': json.dumps(sum(receber_janeiro)),
        'receber_fevereiro':json.dumps(sum(receber_fevereiro)),
        'receber_marco':json.dumps(sum(receber_marco)),
        'receber_abril':json.dumps(sum(receber_abril)),
        'receber_maio':json.dumps(sum(receber_maio)),
        'receber_junho':json.dumps(sum(receber_junho)),
        'receber_julho':json.dumps(sum(receber_julho)),
        'receber_agosto':json.dumps(sum(receber_agosto)),
        'receber_setembro':json.dumps(sum(receber_setembro)),
        'receber_outubro':json.dumps(sum(receber_outubro)),
        'receber_novembro':json.dumps(sum(receber_novembro)),
        'receber_dezembro':json.dumps(sum(receber_dezembro)),
        #saldo
        'saldo_jan':json.dumps(jan),
        'saldo_fev':json.dumps(fev),
        'saldo_mar':json.dumps(mar),
        'saldo_abr':json.dumps(abr),
        'saldo_mai':json.dumps(mai),
        'saldo_jun':json.dumps(jun),
        'saldo_jul':json.dumps(jul),
        'saldo_ago':json.dumps(ago),
        'saldo_setb':json.dumps(setb),
        'saldo_out':json.dumps(out),
        'saldo_nov':json.dumps(nov),
        'saldo_dez':json.dumps(dez),


    }
    return render(request, 'grafico_receitas.html', context)

