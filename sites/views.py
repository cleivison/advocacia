from django.shortcuts import render

# Create your views here.
#home 
def site(request):
    return render(request, 'index.html')
#sobre
def sobre(request):
    return render(request, 'about.html')
#serviços
def servicos(request):
    return render(request, 'services.html')

#contato
def contato(request):
    return render(request, 'contact.html')

def dashboard(request):
    return render(request, 'dashboard.html')

