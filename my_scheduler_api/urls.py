from django.contrib import admin
from django.urls import path, include  # Importe a função include
from django.conf import settings
from django.conf.urls.static import static
from my_scheduler_api import views

app_name = "my_scheduler_api"
urlpatterns = [
    path("my_scheduler_api/", include("my_scheduler_api.urls")), 
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)