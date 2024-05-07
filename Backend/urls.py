"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from my_scheduler_api import views
from django.views.generic import RedirectView

urlpatterns = [
    path("my_scheduler_api/",views.index, name='index'),
    path('my_scheduler_api/register', views.register_or_login, name='register_or_login'),
    path('my_scheduler_api/profile', views.profile, name='profile'),
    path('my_scheduler_api/adminpage/', views.adminpage, name='adminpage'),
    path("my_scheduler_api/logoutview", views.logoutview, name='logoutview'),
    path("my_scheduler_api/fazer_upload", views.fazer_upload, name='fazer_upload'),
    path('my_scheduler_api/create_service', views.create_service, name='create_service'),
    path('my_scheduler_api/update_client', views.update_client, name='update_client'),
    path('my_scheduler_api/aprovar_servico/<int:servico_id>/', views.aprovar_servico, name='aprovar_servico'),
    path('my_scheduler_api/rejeitar_servico/<int:servico_id>/', views.rejeitar_servico, name='rejeitar_servico'),
    path("my_scheduler_api/appointment/<int:servico_id>/",views.appointment, name='appointment'),
    path("my_scheduler_api/serviceDetail/<int:servico_id>/",views.serviceDetail, name='serviceDetail'),
    
    
    path('admin/', admin.site.urls),
    path("my_scheduler_api/services",views.services),
    path("my_scheduler_api/company/<int:company_id>/services",views.company_services),
    path("my_scheduler_api/employees/<int:pk>",views.employee_details),
    path('my_scheduler_api/appointments/<int:pk>', views.appointment_detail),
    path('my_scheduler_api/clients', views.client),
    path('my_scheduler_api/clietns/<int:pk>', views.client_detail),
    path('my_scheduler_api/clients/<int:client_id>/appointments', views.client_appointments),
    path('my_scheduler_api/companies/', views.company_list),
    path('my_scheduler_api/companies/<int:pk>', views.company_detail),
    path("my_scheduler_api/company/<int:company_id>/employees/", views.company_employees),
]
