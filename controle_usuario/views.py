from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from global_permissions.models import GlobalPermission
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from .forms import *
from .models import *


@login_required(login_url='/usuario/login/')
@permission_required('request.user.is_superuser', login_url='/usuario/login/')
def registro_usuario(request):

    if request.method == 'POST':

        form = funcionarioForm(request.POST)

        if form.is_valid():

            func = form.save(commit=False)

            cadastrar_permissoes()

            user = User.objects.create_user(
                first_name=request.POST['nome'],
                last_name=request.POST['sobrenome'],
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['username'],
                is_superuser=False,
                is_staff=True,
            )

            if func.perfil == 'Administrador':
                permission = Permission.objects.get(codename='cadastro')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='agenda')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='diario')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='processos')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='controle_usuario')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='blog')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='financeiro')
                user.user_permissions.add(permission)

            elif func.perfil == 'Atendente':
                permission = Permission.objects.get(codename='cadastro')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='agenda')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='diario')
                user.user_permissions.add(permission)

            elif func.perfil == 'Advogado':
                permission = Permission.objects.get(codename='processos')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='agenda')
                user.user_permissions.add(permission)
                permission = Permission.objects.get(codename='diario')
                user.user_permissions.add(permission)

            func.user = user
            func.save()

            return redirect('/usuario/')
    else:
        form = funcionarioForm()
    return render(request, 'registro.html', {'form': form})


def cadastrar_permissoes():
    try:
        pers = Permission.objects.get(codename='cadastro')
    except Exception:
        pers = None

    if pers is None:

        GlobalPermission.objects.create(name='cadastro', codename='cadastro')
        GlobalPermission.objects.create(name='agenda', codename='agenda')
        GlobalPermission.objects.create(name='financeiro', codename='financeiro')
        GlobalPermission.objects.create(name='blog', codename='blog')
        GlobalPermission.objects.create(name='processos', codename='processos')
        GlobalPermission.objects.create(name='controle_usuario', codename='controle_usuario')
        GlobalPermission.objects.create(name='diario', codename='diario')


def login_usuario(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
    else:
        if request.user.is_authenticated():
            return redirect('/agenda/')

    return render(request, 'login_usuario.html')


@login_required(login_url='/usuario/login/')
@permission_required('request.user.is_superuser', login_url='/usuario/error/')
def lista_usuario(request):

    try:
        users = User.objects.all()
    except Exception:
        users = None

    context = dict({
        'users': users,
    })
    return render(request, 'usuarios.html', context)


@login_required(login_url='/usuario/login/')
@permission_required('request.user.is_superuser', login_url='/usuario/error/')
def deletar_usuario(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('/usuario/')


def logout_usuario(request):
    logout(request)
    return redirect('/usuario/login/')


def error_usuario(request):
    return render(request, 'error_usuario.html')


def recuperar_senha(request):

    try:

        if request.POST:

            email = request.POST['email']

            user = User.objects.get(email=email)

            if user != None:

                unique_id = get_random_string(length=8)
                email_msg = EmailMessage('Recuperando senha', 'Sua nova senha é:' + unique_id, to=[email])
                email_msg.send()
                user.set_password(unique_id)
                user.save()
                return redirect('/usuario/')

    except Exception:
        pass
    return render(request, 'recuperar_senha.html')


@login_required(login_url='/usuario/login/')
def mudar_senha(request):

    try:

        if request.POST:

            user = User.objects.get(username=request.POST['email'])

            if user.check_password(request.POST['senha_atual']):

                senha_nova = request.POST['nova_senha']
                confirm_senha = request.POST['confirma_senha']

                if senha_nova == confirm_senha:

                    user.set_password(senha_nova)
                    user.save()
                    return redirect('/usuario/')

    except Exception:
        pass

    return render(request, 'mudar_senha.html')
