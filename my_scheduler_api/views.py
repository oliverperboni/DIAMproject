from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Employee
from .serializers import *
from django.http import JsonResponse
from rest_framework.decorators import *




@api_view(['POST','GET'])
def index(request):
    return JsonResponse("My API for DIAM",safe=False)
        
@api_view(['POST','GET'])
def employee(request):
    if request.method == "GET":
        employee=Employee.objects.all()
        serialize = EmployeeSerializer(employee,many=True)
        return JsonResponse(serialize.data,safe=False)
    if request.method == "POST":
        employee = EmployeeSerializer(data=request.data)
        if employee.is_valid() :
            employee.save()
            return JsonResponse("Saved",safe=False)  

@api_view(['POST','GET'])        
def services(request):
    if request.method == "GET":
        Service=Servicos.objects.all()
        serialize = ServiceSerializer(Service,many=True)
        return JsonResponse(serialize.data,safe=False)
    if request.method == "POST":
        Service = ServiceSerializer(data=request.data)
        if Service.is_valid() :
            Service.save()
            return JsonResponse("Saved",safe=False)  

@api_view(['PUT','GET',"DELETE"])  
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

@api_view(['POST','GET'])  
def appointment(request):
    if request.method == "GET":
        appointment =Appointment.objects.all()
        serialize = AppointmentSerializer(appointment,many=True)
        return JsonResponse(serialize.data,safe=False)
    if request.method == "POST":
        print("recebi o post")
        appointment = AppointmentSerializer(data=request.data)
        if appointment.is_valid() :
            print("TESTE")
            appointment.save()
            appointment_data = {
            'message': 'Appointment created successfully!'
            }
            return JsonResponse(appointment_data, status=201)
         # Handle other HTTP methods if necessary
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@api_view(['GET', 'PUT', 'DELETE'])
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

@api_view(['GET', 'PUT', 'DELETE'])
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


@api_view(['GET', 'POST'])
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


@api_view(['GET', 'PUT', 'DELETE'])
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


@api_view(['GET'])
def client_appointments(request, client_id):
    try:
        appointments = Appointment.objects.filter(client_id=client_id)
        serializer = AppointmentSerializer1(appointments, many=True)
        return Response(serializer.data)
    except Appointment.DoesNotExist:
        return Response({"error": "Client appointments not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET', 'POST'])
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

@api_view(['GET', 'PUT', 'DELETE'])
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
    
    
@api_view(['GET'])
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

