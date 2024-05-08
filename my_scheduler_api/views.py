from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .serializers import *


def index(request):
    services = Services.objects.all()
    return render(request, 'index.html', {'services': services})


def register_or_login(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "register":
            # Processamento dos dados do formulário de registro
            name = request.POST["name"]
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
        return redirect('index')


def create_service(request):
    if request.method == 'POST':
        # Coletar os dados do POST
        name = request.POST.get('name')
        selected_times = request.POST.getlist('selectedTimes')
        menu_items_text = request.POST.get('menuItems')
        description = request.POST.get('serviceDescription')
        icon = request.FILES.get('serviceIcon')
        banner = request.FILES.get('serviceBanner')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        location = f"{latitude},{longitude}"

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
            address=location,
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


@login_required
def update_client(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['city']

        try:
            client = Client.objects.get(user=request.user)
            client.name = name
            client.email = email
            client.phone = phone
            client.location = location
            client.save()
        except Client.DoesNotExist:
            client = Client.objects.create(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                location=location
            )

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password and new_password and confirm_password:
            # Verificar se a senha atual está correta
            if request.user.check_password(current_password):
                # Verificar se a nova senha e a confirmação são iguais
                if new_password == confirm_password:
                    # Alterar a senha do usuário
                    request.user.set_password(new_password)
                    request.user.save()
                    # Atualizar a sessão de autenticação do usuário
                    update_session_auth_hash(request, request.user)
        return render(request,
                      'index.html')  # Redirecionar para a página de perfil do usuário após o salvamento/atualização
    else:
        return render(request, 'index.html')  # Renderizar o formulário HTML para atualizar o cliente


def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        if request.user.client:
            request.user.client.image.name = filename  # Salva apenas o nome do arquivo, não o URL completo
            request.user.client.save()
        return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'index.html')


def adminpage(request):
    servicos_pendentes = Services.objects.filter(is_approved=False)
    return render(request, 'adminpage.html', {'servicos_pendentes': servicos_pendentes})


def aprovar_servico(request, servico_id):
    if request.method == 'POST':
        servico = Services.objects.get(pk=servico_id)
        servico.is_approved = True
        servico.save()
        return JsonResponse({'message': 'Serviço aprovado com sucesso!'})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)


def rejeitar_servico(request, servico_id):
    if request.method == 'POST':
        servico = get_object_or_404(Services, pk=servico_id)
        servico.delete()  # Excluir o serviço
        return HttpResponse('Serviço rejeitado e excluído com sucesso!')
    else:
        return HttpResponse('Método não permitido', status=405)


def appointment(request, servico_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            client = request.user.client
            name = client.name
            email = client.email
            phone = client.phone
        else:
            client = None
            name = request.POST.get('nome')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

        service = get_object_or_404(Services, pk=servico_id)
        date = request.POST.get('data')
        time = request.POST.get('selected_times2')
        menu_items = request.POST.get('menuItems2')

        appointment = Appointment.objects.create(client=client, service=service, date=date, time=time,
                                                 menuItems=menu_items, name=name, email=email, phone=phone)
        appointment.save()
        return JsonResponse({'message': 'Compromisso criado com sucesso!'})
    else:
        service = get_object_or_404(Services, pk=servico_id)
        return render(request, 'appointment.html', {'servico': service})


def service_detail(request, servico_id):
    service = Services.objects.get(pk=servico_id)
    reviews = service.review_set.all()
    return render(request, 'serviceDetail.html', {'servico': service, 'reviews': reviews})


def add_review(request, servico_id):
    if request.method == 'POST':
        # Verificar se o cliente está autenticado
        if request.user.is_authenticated:
            # Cliente está logado, obter informações do cliente
            client = request.user.client  # Acessar o perfil do cliente associado ao usuário logado

            rating = request.POST.get('rating')
            description = request.POST.get('description')
            service = get_object_or_404(Services, pk=servico_id)

            review = Review(client=client, service=service, description=description, stars=rating)

            # Salvar a revisão no banco de dados
            review.save()
            return JsonResponse({'message': 'Compromisso criado com sucesso!'})

        else:
            # Se o cliente não estiver autenticado, retornar uma resposta de erro
            return JsonResponse({'error': 'O cliente deve estar autenticado para adicionar uma revisão'}, status=401)
    else:
        # Se o método da solicitação não for POST, retornar uma resposta de erro
        return JsonResponse({'error': 'Método não permitido'}, status=405)


def like_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.like()  # Chama o método 'like' na revisão
    return JsonResponse({'message': 'Like adicionado com sucesso!'})


def dislike_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.dislike()  # Chama o método 'dislike' na revisão
    return JsonResponse({'message': 'Dislike adicionado com sucesso!'})
