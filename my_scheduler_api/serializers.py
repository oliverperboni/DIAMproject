from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):

    # employee = EmployeeSerializer()
    # service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"

class AppointmentSerializer1(serializers.ModelSerializer):

    employee = EmployeeSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
        
class ClientSerializer(serializers.ModelSerializer): 
    class Meta:
            model = Client
            fields = "__all__"
 
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company  
        fields = "__all__"         