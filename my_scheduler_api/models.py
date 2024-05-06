from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Company(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    workDays = models.JSONField() 
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee')
    image = models.ImageField(default="static/media/profile_default.png")


    def __str__(self):
        return f"Employee {self.id}: {self.name}"
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=50)
    image = models.ImageField(default="static/media/profile_default.png")
    
    def __str__(self):
        return f"client {self.id}: {self.name}"

class Services(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    selected_times = models.JSONField()
    menuItems = models.JSONField() 
    description = models.TextField()
    icon = models.ImageField(default="static/media/profile_default.png")
    banner = models.ImageField(default="static/media/profile_default.png")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Service {self.id}: {self.name} - Client: {self.client.name}"

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    menuItems = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Appointment {self.id} -  with {self.employee.name} for {self.service.name} on {self.date} at {self.time}"
    
    

