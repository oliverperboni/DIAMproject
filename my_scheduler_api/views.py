from venv import logger
from django.shortcuts import redirect, render
from Backend.auth_backends.custom_auth_backend import EmailAuthBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Employee
from .serializers import *
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import *

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
        return index(request)
    
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

def services(request):
    if request.method == "GET":
        Service=Services.objects.all()
        serialize = ServiceSerializer(Service,many=True)
        return JsonResponse(serialize.data,safe=False)
    if request.method == "POST":
        Service = ServiceSerializer(data=request.data)
        if Service.is_valid() :
            Service.save()
            return JsonResponse("Saved",safe=False)  

def employee_details(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serialize = EmployeeSerializer(employee, many=False)
        return Response(serialize.data)
    elif request.method == "PUT":
        serialize = EmployeeSerializer(employee, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data)
        return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

def appointment(request):
    return render(request, 'appointment.html')
    
def service_detail(request, pk):
    try:
        service = Servicos.objects.get(pk=pk)
    except Servicos.DoesNotExist:
        return Response({"error": "Service does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def appointment_detail(request, pk):
    try:
        appointment = Appointment.objects.get(pk=pk)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def client(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({"error": "Client does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def client_appointments(request, client_id):
    try:
        appointments = Appointment.objects.filter(client_id=client_id)
        serializer = AppointmentSerializer1(appointments, many=True)
        return Response(serializer.data)
    except Appointment.DoesNotExist:
        return Response({"error": "Client appointments not found"}, status=status.HTTP_404_NOT_FOUND)



def company_list(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def company_detail(request, pk):
    try:
        company = Company.objects.get(pk=pk)
    except Company.DoesNotExist:
        return JsonResponse({'error': 'Company does not exist'}, status=404)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        company.delete()
        return JsonResponse({'message': 'Company deleted successfully'}, status=204)
    
    
def company_services(request, company_id):
    try:
        services = Servicos.objects.filter(company_id=company_id)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Servicos.DoesNotExist:
        return Response({"error": "Services for this company not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def company_employees(request, company_id):
    try:
        employees = Employee.objects.filter(company_id=company_id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({"error": "Employees for this company not found"}, status=status.HTTP_404_NOT_FOUND)

