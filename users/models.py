import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Customizando o modelo de usuário
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    roles = models.ManyToManyField(Role, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    

# Opções de gênero
GENDERS = [
    ("Masculino", "Masculino"),
    ("Feminino", "Feminino"),
    ("Não-binário", "Não-binário"),
    ("Outro", "Outro"),
]

# Opções de sexo de nascimento
BIRTH_SEX = [
    ("M", "Masculino"),
    ("F", "Feminino"),
]


# Modelo de perfil do usuário
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    social_name = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birthday_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # Campos obrigatórios de gênero e sexo de nascimento
    gender = models.CharField(max_length=15, choices=GENDERS, blank=True, null=True)
    birth_sex = models.CharField(max_length=1, choices=BIRTH_SEX, blank=True, null=True)

    code_nr = models.CharField(max_length=50, blank=True, null=True)
    code_senior = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
