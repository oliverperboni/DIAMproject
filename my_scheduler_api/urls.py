from django.urls import path
from . import views

app_name = 'my_scheduler_api'
urlpatterns = [

    path('', views.index, name="index"),
    path('register', views.register_or_login, name='register_or_login'),
    path('profile', views.profile, name='profile'),
    path('adminpage', views.adminpage, name='adminpage'),
    path('logoutview', views.logoutview, name='logoutview'),
    path('fazer_upload', views.fazer_upload, name='fazer_upload'),
    path('create_service', views.create_service, name='create_service'),
    path('update_client', views.update_client, name='update_client'),
    path('aprovar_servico/<int:servico_id>', views.aprovar_servico, name='aprovar_servico'),
    path('rejeitar_servico/<int:servico_id>', views.rejeitar_servico, name='rejeitar_servico'),
    path('appointment/<int:servico_id>', views.appointment, name='appointment'),
    path('serviceDetail/<int:servico_id>', views.service_detail, name='serviceDetail'),
    path('add_review/<int:servico_id>', views.add_review, name='add_review'),
    path('like_review/<int:review_id>', views.like_review, name='like_review'),
    path('dislike_review/<int:review_id>', views.dislike_review, name='dislike_review'),

]
