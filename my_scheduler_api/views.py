from venv import logger
from django.shortcuts import get_object_or_404, redirect, render
from Backend.auth_backends.custom_auth_backend import EmailAuthBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Employee
from .serializers import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import *
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def register_or_login(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "register":
            # Processamento dos dados do formulário de registro
            name=request.POST["name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            location = request.POST["location"]
            phone = request.POST["phone"]

            user = User.objects.create_user(username=username, email=email, password=password)
            client = Client.objects.create(user=user, name=name, email=email, phone=phone, location=location)
            client.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return index(request)
        elif action == "login":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id 
                return index(request)
            else:
                return index(request)
    else:
        return render(request, "register.html")
    

def logoutview(request):
    if request.method == "GET":
        request.session.flush()
        logout(request)
        return redirect('index')
    
def create_service(request):
    if request.method == 'POST':
        # Coletar os dados do POST
        name = request.POST.get('name')
        selected_times = request.POST.getlist('selectedTimes')
        menu_items_text = request.POST.get('menuItems')
        description = request.POST.get('serviceDescription')
        icon = request.FILES.get('serviceIcon')
        banner = request.FILES.get('serviceBanner')
        
        menu_items_list = menu_items_text.splitlines()
        menu_items = [item.strip() for item in menu_items_list if item.strip()]
        
        # Salvar os dados no banco de dados
        service = Services.objects.create(
            name=name,
            selected_times=selected_times,
            menuItems=menu_items,
            description=description,
            icon=icon,
            banner=banner,
            client=request.user.client
        )
        service.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': True})

def profile(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        client = None
    context = {
        'client': client
    }
    return render(request, "profile.html", context)

@login_required
def update_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['city']
        
        try:
            client = Client.objects.get(user=request.user)
            client.name = name
            client.email = email
            client.phone = phone
            client.location = location
            client.save()
        except Client.DoesNotExist:
            client = Client.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                location=location
            )
            
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            # Verificar se a senha atual está correta
            if request.user.check_password(current_password):
                # Verificar se a nova senha e a confirmação são iguais
                if new_password == confirm_password:
                    # Alterar a senha do usuário
                    request.user.set_password(new_password)
                    request.user.save()
                    # Atualizar a sessão de autenticação do usuário
                    update_session_auth_hash(request, request.user)
        return render(request, 'index.html')  # Redirecionar para a página de perfil do usuário após o salvamento/atualização
    else:
        return render(request, 'index.html')  # Renderizar o formulário HTML para atualizar o cliente

def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if request.user.client:
            request.user.client.image.name = filename  # Salva apenas o nome do arquivo, não o URL completo
            request.user.client.save()
        return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'index.html')

def adminpage(request):
    servicos_pendentes = Services.objects.filter(is_approved=False)
    return render(request, 'adminpage.html', {'servicos_pendentes': servicos_pendentes})

def aprovar_servico(request, servico_id):
    if request.method == 'POST':
        servico = Services.objects.get(pk=servico_id)
        servico.is_approved = True
        servico.save()
        return JsonResponse({'message': 'Serviço aprovado com sucesso!'})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
def rejeitar_servico(request, servico_id):
    if request.method == 'POST':
        servico = get_object_or_404(Services, pk=servico_id)
        servico.delete()  # Excluir o serviço
        return HttpResponse('Serviço rejeitado e excluído com sucesso!')
    else:
        return HttpResponse('Método não permitido', status=405)




@api_view(['GET'])
def client_appointments(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    appointments = Appointment.objects.filter(client=client)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_service_appointments(request, client_id, service_id):
    client = get_object_or_404(Client, pk=client_id)
    service = get_object_or_404(Services, pk=service_id, client=client)
    appointments = Appointment.objects.filter(client=client, service=service)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employee_appointments(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    appointments = Appointment.objects.filter(employee=employee)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Extrair dados do corpo da solicitação
        data = json.loads(request.body)
        username = data.get('email', None)
        password = data.get('password', None)
        
        # Autenticar o usuário
        user = authenticate(username=username, password=password)
        
        # Verificar se a autenticação foi bem-sucedida
        if user is not None:
            login(request, user)
            # Retornar o ID do cliente se disponível
            client_id = user.client.id if hasattr(user, 'client') else None
            return JsonResponse({'message': 'Login bem-sucedido', 'client_id': client_id})
        else:
            return JsonResponse({'message': 'Credenciais inválidas'}, status=401)
    
    else:
        return JsonResponse({'message': 'Método não permitido'}, status=405)

