from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from financeiro.models import *
import json

@login_required(login_url='/usuario/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

