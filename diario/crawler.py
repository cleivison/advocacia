import requests
import sys
from bs4 import BeautifulSoup
import PyPDF2
import re

def buscar_documento(data):

    payload = {'dataDiario': data}
    a = requests.post('http://www.tjpi.jus.br/site/modules/diario/Init.download.mtw', data=payload)
    soup = BeautifulSoup(a.content)
    #table = soup.find('tbody',id='tab-movimentacoes')
    table = soup.find('table')
    #table = soup.find('tbody')

    texto = []
    for line in table.findAll('a'):
        texto.append(line.get('href'))

    return texto


def buscar_texto(arquivo, conteudo):

    pagina = []
    file = open(arquivo,'rb')
    pdfDoc = PyPDF2.PdfFileReader(file)
    for i in range(0, pdfDoc.getNumPages()):
        content = ""
        content += pdfDoc.getPage(i).extractText() + "\n"
        content = content.lower()
        conteudo = conteudo.lower()
        ResSearch = re.search(conteudo, content)
        if ResSearch is not None:
           pagina.append(i)           

    file.close()
    return pagina
