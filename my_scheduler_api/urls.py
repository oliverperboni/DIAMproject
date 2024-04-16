from django.contrib import admin
from django.urls import path, include  # Importe a função include
from my_scheduler_api import views

app_name = "my_scheduler_api"
urlpatterns = [
    path("my_scheduler_api/", include("my_scheduler_api.urls")), 
    path('admin/', admin.site.urls),
]
