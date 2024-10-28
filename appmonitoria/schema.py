import graphene
from graphene_django.types import DjangoObjectType
from users.models import CustomUser, Profile

# Definindo tipos GraphQL para CustomUser e Profile
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'roles', 'created_at', 'updated_at')

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'cpf', 'photo', 'created_at', 'updated_at', 'user')

# Definindo as Queries
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int())
    all_profiles = graphene.List(ProfileType)

    def resolve_all_users(root, info):
        return CustomUser.objects.all()

    def resolve_user_by_id(root, info, id):
        return CustomUser.objects.get(pk=id)

    def resolve_all_profiles(root, info):
        return Profile.objects.all()

# Mutations para criar ou atualizar usuários (opcional)
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, email):
        user = CustomUser(username=username, email=email)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# Definindo o schema completo com Query e Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
