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
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('my_scheduler_api/', include('my_scheduler_api.urls')),
    path('admin/', admin.site.urls),
    # path("my_scheduler_api/services",views.services),
    # path("my_scheduler_api/company/<int:company_id>/services",views.company_services),
    # path("my_scheduler_api/appointment",views.appointment, name='appointment'),
    # path("my_scheduler_api/employees/<int:pk>",views.employee_details),
    # path('my_scheduler_api/services/<int:pk>', views.service_detail),
    # path('my_scheduler_api/appointments/<int:pk>', views.appointment_detail),
    # path('my_scheduler_api/clients', views.client),
    # path('my_scheduler_api/clietns/<int:pk>', views.client_detail),
    # path('my_scheduler_api/clients/<int:client_id>/appointments', views.client_appointments),
    # path('my_scheduler_api/companies/', views.company_list),
    # path('my_scheduler_api/companies/<int:pk>', views.company_detail),
    # path("my_scheduler_api/company/<int:company_id>/employees/", views.company_employees),
    path('clients/<int:client_id>/appointments/', views.client_appointments, name='client_appointments'),
    path('clients/<int:client_id>/services/<int:service_id>/appointments/', views.client_service_appointments, name='client_service_appointments'),
    path('employees/<int:employee_id>/appointments/', views.employee_appointments, name='employee_appointments'),
    path('api/login/', views.login_view, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
