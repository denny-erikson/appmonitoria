import os
import django
import uuid
from faker import Faker
from random import choice, randint, uniform
from django.core.validators import MinValueValidator, MaxValueValidator

# Configurar Django para acessar os modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appmonitoria.settings")  # Ajuste para o nome correto do seu projeto
django.setup()

from django.contrib.auth import get_user_model
from monitoria.models import Category
from users.models import Role, Profile

# Definir models
CustomUser = get_user_model()

# Inicializar Faker
fake = Faker()

# Opções de gênero e sexo
GENDERS = ["Masculino", "Feminino", "Não-binário", "Outro"]
BIRTH_SEX = ["M", "F"]
PROFICIENCY_CHOICES = ["B", "I", "A", "F", "N"]

# Criar Roles
def criar_roles():
    roles_nomes = ["Admin", "Usuário", "Moderador", "Editor"]
    roles = [Role.objects.create(name=nome) for nome in roles_nomes]
    print(f"{len(roles)} Roles criadas.")
    return roles

# Criar Categorias
def criar_categorias(qtd=5):
    categorias = []
    for _ in range(qtd):
        categoria = Category.objects.create(
            title=fake.word().capitalize(),
            proficiency=choice(PROFICIENCY_CHOICES),
            amount=round(uniform(100.0, 5000.0), 2),
            percentage=round(uniform(0, 100), 2)
        )
        categorias.append(categoria)
    print(f"{qtd} Categorias criadas.")
    return categorias

# Criar Usuários e Perfis
def criar_usuarios(qtd=10, roles=None, categorias=None):
    usuarios = []
    for _ in range(qtd):
        user = CustomUser.objects.create_user(
            username=fake.user_name(),
            email=fake.unique.email(),
            password="teste123",  # Senha padrão
        )
        user.roles.set([choice(roles)])  # Atribuir um papel aleatório
        user.save()

        # Criar perfil para o usuário
        Profile.objects.create(
            user=user,
            name=fake.name(),
            social_name=fake.first_name(),
            birthday_date=fake.date_of_birth(minimum_age=18, maximum_age=30),
            gender=choice(GENDERS),
            birth_sex=choice(BIRTH_SEX),
            code_nr=str(uuid.uuid4())[:8],  # Gerar código aleatório
            code_senior=str(uuid.uuid4())[:8],
            category=choice(categorias) if categorias else None
        )
        usuarios.append(user)

    print(f"{qtd} Usuários e Perfis criados.")

# Rodar funções
if __name__ == "__main__":
    roles = criar_roles()
    categorias = criar_categorias(5)
    criar_usuarios(20, roles, categorias)
