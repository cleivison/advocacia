import requests
import sys
from bs4 import BeautifulSoup
from .models import Processo_trabalhista, Movimento_trab
import PyPDF2
import datetime

def add_processo_trab(pr, cliente, advogado):

    payload = {'NumPro': pr[0] , 'AnoPro': pr[1], 'VVV': pr[2], 'RR': pr[3], 'SS': pr[4]}
    a = requests.post('http://aptv.trt22.jus.br/consulta/MovProJVaras.jsp', data=payload)
    soup = BeautifulSoup(a.content)
    table = soup.find('table',id='cabecalho')
    row = table.findAll("td")

    p = Processo_trabalhista()
    p.especie = row[1].text
    p.reclamante = row[2].text
    p.advogado_reclamante = row[3].text
    p.reclamado = row[4].text
    p.advogado_reclamado = row[5].text
    p.etapa_processo = row[6].text

    p.numero_processo = pr[0]
    p.ano_processo = pr[1]
    p.VVV = pr[2]
    p.RR = pr[3]
    p.SS = pr[4]

    p.cliente = cliente
    p.usuario = advogado

    p.save()

    table2 = soup.find_all('tr')

    for i in range(14, len(table2)-1):
        row_m = table2[i].findAll("td")
        m = Movimento_trab()
        print(row_m[0].text+'\n')
        m.data_movimentacao = datetime.datetime.strptime(row_m[0].text, '%d/%m/%Y').strftime('%Y-%m-%d')
        m.descricao = row_m[1].text
        m.processo = p
        #m.doc = row_m[2].find('a')['href']
        m.save()
