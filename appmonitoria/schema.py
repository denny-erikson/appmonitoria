import graphql_jwt
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from users.models import CustomUser, Profile
from events.models import Availability, Event


# Definindo tipos GraphQL para CustomUser e Profile
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'roles', 'created_at', 'updated_at')

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('id', 'name', 'cpf', 'photo', 'created_at', 'updated_at', 'user')

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'end_date', 'daily', 'resort')

    # Convertendo snake_case para camelCase para seguir convenções GraphQL
    start_date = graphene.String()
    end_date = graphene.String()

    def resolve_start_date(self, info):
        return self.start_date.isoformat() if self.start_date else None

    def resolve_end_date(self, info):
        return self.end_date.isoformat() if self.end_date else None

class AvailabilityType(DjangoObjectType):
    class Meta:
        model = Availability
        fields = '__all__'

class EventPaginationType(graphene.ObjectType):
    items = graphene.List(EventType)
    total_count = graphene.Int()
    has_next_page = graphene.Boolean()

# Definindo as Queries
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int())
    all_profiles = graphene.List(ProfileType)
    all_events = graphene.Field(
        EventPaginationType,
        offset=graphene.Int(),
        limit=graphene.Int(),
        name=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String(),
        order_by=graphene.String()
    )
    total_events = graphene.Int()
    all_availability = graphene.List(AvailabilityType)
    event_by_id = graphene.Field(EventType, id=graphene.ID(required=True))

    def resolve_all_users(root, info):
        return CustomUser.objects.all()

    def resolve_user_by_id(root, info, id):
        return CustomUser.objects.get(pk=id)

    def resolve_all_profiles(root, info):
        return Profile.objects.all()
    
    @login_required
    def resolve_all_events(root, info, offset=None, limit=None, name=None, 
                         start_date=None, end_date=None, order_by=None):
        # Começamos com todos os eventos
        queryset = Event.objects.all()

        # Aplicamos os filtros
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        # Aplicamos a ordenação
        if order_by:
            # Verificamos se é ordenação descendente
            if order_by.startswith('-'):
                order_field = order_by[1:]
                if hasattr(Event, order_field):
                    queryset = queryset.order_by(order_by)
            else:
                if hasattr(Event, order_by):
                    queryset = queryset.order_by(order_by)

        # Calculamos o total antes da paginação
        total_count = queryset.count()

        # Aplicamos a paginação
        if offset is not None and limit is not None:
            queryset = queryset[offset:offset + limit]
            has_next_page = total_count > (offset + limit)
        else:
            has_next_page = False

        return EventPaginationType(
            items=queryset,
            total_count=total_count,
            has_next_page=has_next_page
        )
    
    def resolve_total_events(root, info):
        return Event.objects.count()

    def resolve_all_availability(root, info):
        return Availability.objects.all()

    @login_required
    def resolve_event_by_id(root, info, id):
        try:
            return Event.objects.get(pk=id)
        except Event.DoesNotExist:
            return None

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
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()

# Definindo o schema completo com Query e Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
