from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Company(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)

    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name


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
    address = models.CharField(max_length=255)
    icon = models.ImageField(default="static/media/profile_default.png")
    banner = models.ImageField(default="static/media/profile_default.png")
    is_approved = models.BooleanField(default=False)

    def calculate_average_rating(self):
        # Obtém todas as revisões associadas a este serviço
        reviews = Review.objects.filter(service=self)

        # Calcula a média das estrelas usando a função Avg do Django
        average_rating = reviews.aggregate(Avg('stars'))['stars__avg']

        # Se não houver revisões ou a média for None, retorna 0
        if average_rating is None:
            return 0
        else:
            return round(average_rating, 1)

    def review_count(self):
        # Filtra as avaliações pelo ID do serviço atual
        reviews = Review.objects.filter(service=self)
        # Conta o número de avaliações
        count = reviews.count()
        return count

    def __str__(self):
        return f"Service {self.id}: {self.name} - Client: {self.client.name}"

# OLI 11/05/2024
# class Review(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     service = models.ForeignKey(Services, on_delete=models.CASCADE)
#     description = models.TextField()
#     stars = models.SmallIntegerField()
#     likes = models.BigIntegerField(default=0)
#     dislikes = models.BigIntegerField(default=0)

#     def like(self):
#         self.likes += 1
#         self.save(update_fields=['likes'])

#     def dislike(self):
#         self.dislikes += 1
#         self.save(update_fields=['dislikes'])

#     def __str__(self):
#         return f"Review {self.id}: {self.client.name} - {self.service.name}"


class Review(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    description = models.TextField()
    stars = models.SmallIntegerField()
    likes = models.BigIntegerField(default=0)
    dislikes = models.BigIntegerField(default=0)

    def like(self, user):
        clientToAdd = Client.objects.get(id=user)
        if not Like.objects.filter(review=self, client=clientToAdd).exists():
            Like.objects.create(review=self, client=clientToAdd, is_like=True)
            self.likes += 1
            self.dislikes -= 1
            self.save(update_fields=['likes'])
            self.save(update_fields=['dislikes'])
            return True
        return False

    def dislike(self, user):
        clientToAdd = Client.objects.get(id=user)
        if Like.objects.filter(review=self, client=clientToAdd).exists():
            like_objeto = Like.objects.filter(review=self, client=clientToAdd)
            like_objeto.delete() 
            self.likes -= 1
            self.dislikes += 1
            self.save(update_fields=['likes'])
            self.save(update_fields=['dislikes'])
            return True
        return False

    def __str__(self):
        return f"Review {self.id}: {self.client.name} - {self.service.name}"

class Like(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)  # True para like, False para dislike

    class Meta:
        unique_together = ('review', 'client')  # Garante que um usuário só pode dar um like ou dislike uma vez por revisão



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
        return f"Appointment {self.id} -  with {self.client.name} for {self.service.name} on {self.date} at {self.time}"
