import graphql_jwt
import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from users.models import CustomUser, Profile
from events.models import Availability, Event, Team
from monitoria.models import Rating


# Definindo tipos GraphQL para CustomUser e Profile
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'roles', 'created_at', 'updated_at')

class AvailabilityType(DjangoObjectType):
    class Meta:
        model = Availability
        fields = '__all__'

class ProfileType(DjangoObjectType):
    rating_stats = graphene.Field(graphene.JSONString)
    rating_distribution = graphene.Field(graphene.JSONString)
    availabilities = graphene.List(AvailabilityType)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'cpf', 'photo', 'created_at', 'updated_at', 'user', 'ratings')

    def resolve_rating_stats(self, info):
        return self.get_rating_stats()

    def resolve_rating_distribution(self, info):
        return self.get_rating_distribution()

    def resolve_availabilities(self, info):
        return Availability.objects.filter(profile=self)

class RatingType(DjangoObjectType):
    score_display = graphene.String()

    class Meta:
        model = Rating
        fields = ('id', 'profile', 'event', 'score', 'description', 
                 'created_at', 'updated_at', 'created_by')

    def resolve_score_display(self, info):
        return self.score_display

class EventType(DjangoObjectType):
    ratings_by_event = graphene.List(RatingType)

    class Meta:
        model = Event
        fields = ('id', 'name', 'start_date', 'end_date', 'daily', 'resort', 'ratings')

    # Convertendo snake_case para camelCase para seguir convenções GraphQL
    start_date = graphene.String()
    end_date = graphene.String()

    def resolve_start_date(self, info):
        return self.start_date.isoformat() if self.start_date else None

    def resolve_end_date(self, info):
        return self.end_date.isoformat() if self.end_date else None

    def resolve_ratings_by_event(self, info):
        return self.ratings.all()

class TeamType(DjangoObjectType):
    members_count = graphene.Int()
    availabilities = graphene.List(AvailabilityType)

    class Meta:
        model = Team
        fields = ('id', 'name', 'event', 'status', 'max_availabilities', 'availabilities')

    def resolve_members_count(self, info):
        return self.availabilities.filter(status=True).count()

    def resolve_availabilities(self, info):
        return self.availabilities.all()

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
    all_teams = graphene.List(
        TeamType,
        event_id=graphene.ID()
    )
    team_by_id = graphene.Field(
        TeamType,
        id=graphene.ID(required=True)
    )
    all_availability = graphene.List(
        AvailabilityType,
        team_id=graphene.ID(),
        profile_id=graphene.ID()
    )
    event_by_id = graphene.Field(EventType, id=graphene.ID(required=True))
    ratings_by_event = graphene.List(
        RatingType, 
        event_id=graphene.ID(required=True)
    )
    ratings_by_profile = graphene.List(
        RatingType, 
        profile_id=graphene.ID(required=True)
    )
    rating_by_id = graphene.Field(
        RatingType, 
        id=graphene.ID(required=True)
    )
    user_profile = graphene.Field(
        ProfileType,
        id=graphene.ID(required=True)
    )
    my_profile = graphene.Field(ProfileType)

    def resolve_all_users(root, info):
        return CustomUser.objects.all()

    def resolve_user_by_id(root, info, id):
        return CustomUser.objects.get(pk=id)

    def resolve_all_profiles(root, info):
        return Profile.objects.all()
    

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

    #@login_required
    def resolve_all_teams(root, info, event_id=None):
        queryset = Team.objects.all()
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset

  
    def resolve_team_by_id(root, info, id):
        try:
            return Team.objects.get(pk=id)
        except Team.DoesNotExist:
            return None

    @login_required
    def resolve_all_availability(root, info, team_id=None, profile_id=None):
        queryset = Availability.objects.all()
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        if profile_id:
            queryset = queryset.filter(profile_id=profile_id)
        return queryset

    @login_required
    def resolve_event_by_id(root, info, id):
        try:
            return Event.objects.get(pk=id)
        except Event.DoesNotExist:
            return None

    @login_required
    def resolve_ratings_by_event(root, info, event_id):
        return Rating.objects.filter(event_id=event_id)

    @login_required
    def resolve_ratings_by_profile(root, info, profile_id):
        return Rating.objects.filter(profile_id=profile_id)

    @login_required
    def resolve_rating_by_id(root, info, id):
        try:
            return Rating.objects.get(pk=id)
        except Rating.DoesNotExist:
            return None

    @login_required
    def resolve_user_profile(root, info, id):
        try:
            return Profile.objects.get(pk=id)
        except Profile.DoesNotExist:
            return None

    @login_required
    def resolve_my_profile(root, info):
        try:
            return Profile.objects.get(user=info.context.user)
        except Profile.DoesNotExist:
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

# Mutations para Rating
class CreateRating(graphene.Mutation):
    class Arguments:
        profile_id = graphene.ID(required=True)
        event_id = graphene.ID(required=True)
        score = graphene.Int(required=True)
        description = graphene.String(required=True)

    rating = graphene.Field(RatingType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, profile_id, event_id, score, description):
        try:
            # Verificar se já existe uma avaliação
            existing_rating = Rating.objects.filter(
                profile_id=profile_id,
                event_id=event_id
            ).exists()

            if existing_rating:
                return CreateRating(
                    success=False,
                    message="Já existe uma avaliação para este perfil neste evento"
                )

            rating = Rating.objects.create(
                profile_id=profile_id,
                event_id=event_id,
                score=score,
                description=description,
                created_by=info.context.user
            )
            
            return CreateRating(
                rating=rating,
                success=True,
                message="Avaliação criada com sucesso"
            )
        except Exception as e:
            return CreateRating(
                success=False,
                message=str(e)
            )

class UpdateRating(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        score = graphene.Int()
        description = graphene.String()

    rating = graphene.Field(RatingType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, id, score=None, description=None):
        try:
            rating = Rating.objects.get(pk=id)
            
            if score is not None:
                rating.score = score
            if description is not None:
                rating.description = description
                
            rating.save()
            
            return UpdateRating(
                rating=rating,
                success=True,
                message="Avaliação atualizada com sucesso"
            )
        except Rating.DoesNotExist:
            return UpdateRating(
                success=False,
                message="Avaliação não encontrada"
            )

class CreateTeam(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        max_availabilities = graphene.Int()

    team = graphene.Field(TeamType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, event_id, name, max_availabilities=20):
        try:
            event = Event.objects.get(pk=event_id)
            team = Team.objects.create(
                event=event,
                name=name,
                max_availabilities=max_availabilities
            )
            return CreateTeam(
                team=team,
                success=True,
                message="Time criado com sucesso"
            )
        except Exception as e:
            return CreateTeam(
                success=False,
                message=str(e)
            )

class CreateAvailability(graphene.Mutation):
    class Arguments:
        team_id = graphene.ID(required=True)
        profile_id = graphene.ID(required=True)

    availability = graphene.Field(AvailabilityType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, team_id, profile_id):
        try:
            team = Team.objects.get(pk=team_id)
            profile = Profile.objects.get(pk=profile_id)

            # Verificar se já existe disponibilidade
            if Availability.objects.filter(team=team, profile=profile).exists():
                return CreateAvailability(
                    success=False,
                    message="Você já se inscreveu neste time"
                )

            # Verificar se o time está fechado
            if team.status:
                return CreateAvailability(
                    success=False,
                    message="Este time não está mais aceitando inscrições"
                )

            availability = Availability.objects.create(
                team=team,
                profile=profile,
                status=True
            )
            
            return CreateAvailability(
                availability=availability,
                success=True,
                message="Inscrição realizada com sucesso"
            )
        except Exception as e:
            return CreateAvailability(
                success=False,
                message=str(e)
            )

class UpdateAvailabilitySummoned(graphene.Mutation):
    class Arguments:
        availability_id = graphene.ID(required=True)
        summoned = graphene.Boolean(required=True)

    availability = graphene.Field(AvailabilityType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, availability_id, summoned):
        try:
            availability = Availability.objects.get(pk=availability_id)
            availability.summoned = summoned
            availability.save()
            
            return UpdateAvailabilitySummoned(
                availability=availability,
                success=True,
                message="Status de convocação atualizado com sucesso"
            )
        except Exception as e:
            return UpdateAvailabilitySummoned(
                success=False,
                message=str(e)
            )

class CreateProfile(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        cpf = graphene.String(required=True)

    profile = graphene.Field(ProfileType)
    success = graphene.Boolean()
    message = graphene.String()

    @login_required
    def mutate(self, info, name, cpf):
        try:
            profile = Profile.objects.create(
                user=info.context.user,
                name=name,
                cpf=cpf
            )
            return CreateProfile(
                profile=profile,
                success=True,
                message="Perfil criado com sucesso"
            )
        except Exception as e:
            return CreateProfile(
                success=False,
                message=str(e)
            )

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    create_rating = CreateRating.Field()
    update_rating = UpdateRating.Field()
    create_team = CreateTeam.Field()
    create_availability = CreateAvailability.Field()
    update_availability_summoned = UpdateAvailabilitySummoned.Field()
    create_profile = CreateProfile.Field()

# Definindo o schema completo com Query e Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
