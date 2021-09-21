from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from global_permissions.models import GlobalPermission
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from .crawler import *
from .models import Pesquisa
import wget
import requests
import sys
import codecs
import os
import PyPDF2
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


# Create your views here.
@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.diario', login_url='/usuario/error/')
#view que lista os arquivos do diario
def listar(request):
    try:
        path = os.path.join('./media/'+request.user.username)
        file_list = os.listdir(path)
        p = Pesquisa.objects.all().order_by('-id')
        files = zip(file_list, p)
        return render(request, 'diarios.html',{'files': files})
    except Exception:
        return render(request, 'diarios.html')        


def open_pdf(request, pk):

    p = Pesquisa.objects.get(id=pk)
    with open('./media/'+request.user.username+'/'+p.nome_arquivo,'rb')  as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.diario', login_url='/usuario/error/')
def busca_diario(request):

    if request.method == 'POST':

        try:
            file_url = buscar_documento(request.POST.get('data'))
            print(file_url)

            for file_url_list in file_url:
                file_name = wget.download(file_url_list)
                p = Pesquisa()
                p.nome_arquivo  = str(file_name)[:-4]
                p.busca_diario  = request.POST.get('nome')
                p.data = datetime.datetime.now()
                p.save()
                p.nome_arquivo += '_'+str(p.id)+'.pdf'
                #newfile = open('hello.txt','w',encoding='utf-8')
                file = open(file_name,'rb')
                reader = PyPDF2.PdfFileReader(file)
                #page = reader.getPage(1)
                #texto = page.extractText()
                i = buscar_texto(file_name,request.POST.get('nome'))

                try:
                    os.mkdir(os.path.join('./media', request.user.username))
                except OSError as e:
                    pass

                novo_arquivo = open('./media/'+request.user.username+ '/'+p.nome_arquivo,'wb')

                pdfWriter = PyPDF2.PdfFileWriter()

                for pages in i:
                    page = reader.getPage(pages)
                    pdfWriter.addPage(page)

                pdfWriter.write(novo_arquivo)

                file.close()
                novo_arquivo.close()
                os.remove(file_name)
                #newfile.write(page.extractText())
                p.save()
                os.startfile(os.path.join('./media/'+request.user.username, p.nome_arquivo))
        except Exception as e:#
            texto = e

        #return render(request, 'home.html', {'texto' : texto})
    return redirect("/diario/")


@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.diario', login_url='/usuario/error/')
def deletar_diario(request, pk):
    p = Pesquisa.objects.get(id=pk)
    data = dict()
    if request.method == 'POST':
        os.remove(os.path.join('./media/'+request.user.username,p.nome_arquivo ))
        p.delete()
        data['form_is_valid'] = True
        return redirect('/diario/')
    else:
        context = {'pesquisa': p}
        data['html_form'] = render_to_string('deletar.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='/usuario/login/')
@permission_required('global_permissions.diario', login_url='/usuario/error/')
def trt22(request):
    
    if request.method == 'POST':
        path = os.path.join('./media/')
        os.environ['MOZ_HEADLESS'] = '1'
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.dir",os.getcwd()+"\\media")
        fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

        driver = webdriver.Firefox(fp)
        driver.implicitly_wait(30)
        driver.get("http://dejt.jt.jus.br/dejt/f/n/diariocon")
        before = os.listdir(path)
        assert "Pesquisar Diários" in driver.title

        elem = driver.find_element_by_id("corpo:formulario:dataIni")
        elem.clear()
        elem.send_keys(request.POST.get('data'))

        elem = driver.find_element_by_id("corpo:formulario:dataFim")
        elem.clear()
        elem.send_keys(request.POST.get('data'))

        print(request.POST.get('data'))        
        elem = driver.find_element_by_id("corpo:formulario:tipoCaderno")
        elem.send_keys("j")
        driver.implicitly_wait(30)
        sel = Select(driver.find_element_by_id("corpo:formulario:tribunal"))
        sel.select_by_value("22")
        elem.send_keys(Keys.ENTER)        
        driver.save_screenshot('screenie.png')
        driver.implicitly_wait(30)
        elem = driver.find_element_by_class_name("bt.af_commandButton")
        elem.click()

        after = os.listdir(path)
        change = set(after) - set(before)
        print (len(change))
        while True:

            if len(change) != 1:
                after = os.listdir(path)
                change = set(after) - set(before)
                time.sleep(5)
            else:
                break

        print ('passou')
        
        file_name = change.pop()
        print ("arquivo"+file_name)
        driver.quit()

        file = open(path+'/'+file_name,'rb')
        reader = PyPDF2.PdfFileReader(file)
        #page = reader.getPage(1)
        #texto = page.extractText()
        i = buscar_texto(path+'/'+file_name,request.POST.get('nome'))

        try:
            os.mkdir(os.path.join('./media', request.user.username))
        except OSError as e:
            pass

        novo_arquivo = open('./media/'+request.user.username+ '/'+file_name,'wb')

        pdfWriter = PyPDF2.PdfFileWriter()

        for pages in i:
            page = reader.getPage(pages)
            pdfWriter.addPage(page)

        pdfWriter.write(novo_arquivo)

        file.close()
        novo_arquivo.close()
        os.remove(path+'/'+file_name)
        #newfile.write(page.extractText())
        os.startfile(os.path.join('./media/'+request.user.username, file_name))

    return render(request, 'trt22.html')           
