import requests
import sys
from bs4 import BeautifulSoup
from .models import Processo, Partes, Movimento, Distribuicao 
import PyPDF2
import re

def add_piaui_atualiza(p, movimento):      

    payload = {'consulta.numeroUnico': p.numero_processo}
    a = requests.post('http://www.tjpi.jus.br/themisconsulta/consulta/solr/numero', data=payload)
    soup = BeautifulSoup(a.content)
    table = soup.find('tbody',id='tab-movimentacoes')
    row = table.findAll("th")
    row2 = table.findAll("td")

    i = len(row) - len(movimento)

    while( i > 0):
        i -= 1
        m = Movimento()
        m.processo_id = p.id
        m.data_movimentacao = row[i].text
        m.descricao = row2[i].text
        m.save()
        

def add_piaui(pr, cliente, advogado):      

    payload = {'consulta.numeroUnico': pr}
    a = requests.post('http://www.tjpi.jus.br/themisconsulta/consulta/solr/numero', data=payload)
    soup = BeautifulSoup(a.content)
    table = soup.find('div',{"class":"content"})

    table1 = table.findAll("tbody")
    i = 0
    j = 0

    #add processo
    p = Processo()

    if(cliente != ''):
        p.cliente = cliente

    if(advogado != ''):
        p.usuario = advogado

    p.numero_processo = pr

    row = table1[i].findAll("td")
    row2 = table1[i].findAll("th")

    if(row2[0].text == 'Número do Acervo'):        
        p.numero_acervo = row[j].text
        j+=1

    p.data_abertura = row[j].text
    j+=1
    p.comarca = row[j].text
    j+=1
    p.assistencia_judiciaria = row[j].text
    j+=1
    p.natureza = row[j].text
    j+=1
    p.classe_processual = row[j].text
    j+=1
    p.assuntos = row[j].text.strip()
    j+=1
    p.observacao = row[j].text
    j+=1
    p.valor_acao = row[j].text
    j+=1
    p.status_atual = row[j].text
    p.status_processo = True

    p.save()
    i += 1
    #fim do add processo
    #add partes
    row = table1[i].findAll("th")
    if (row[0].text == 'Local'):
        i += 1

    for row,row2 in zip(table1[i].findAll("tr"),table1[i].findAll("th")):
        cells = row.findAll("td")
        partes = Partes()
        partes.processo_id = p.id
        partes.parte = row2.text
        partes.descricao = cells[0].text
        partes.save()

    i += 1
    #fim do add partes
    #add distribuições    
    row = table1[i].findAll("th")
    while(not (row[0].text == 'Realizada')):
        i += 1
        row = table1[i].findAll("th")

    while(row[0].text == 'Realizada'):        
        row = table1[i].findAll("td")

        d = Distribuicao()
        d.processo_id = p.id
        d.realizada = row[0].text
        d.tipo_distribuicao = row[1].text
        d.comarca = row[2].text
        d.secretaria = row[3].text
        d.motivo = row[4].text

        d.save()
        i+= 1
        row = table1[i].findAll("th")
    #fim do add distribuições
    #add movimentações
    table = soup.find('tbody',id='tab-movimentacoes')

    for row,row2 in zip(table.findAll("tr"),table.findAll("th")):
        cells = row.findAll("td")
        m = Movimento()
        m.processo_id = p.id
        m.data_movimentacao = row2.text
        m.descricao = cells[0].text
        m.save()
