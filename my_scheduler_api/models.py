from django.db import models


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


    def __str__(self):
        return f"Employee {self.id}: {self.name}"
    
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"client {self.id}: {self.name}"

class Servicos(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    price = models.FloatField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return f"Service {self.id}: {self.name}"

class Appointment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Servicos, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)

    def __str__(self):
        return f"Appointment {self.id} -  with {self.employee.name} for {self.service.name} on {self.date} at {self.time}"
    
    

