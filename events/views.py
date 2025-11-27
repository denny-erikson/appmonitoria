from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from django.urls import reverse

from events.models import Availability, Cancellation, Event, Product, Resort, Team
from events.serializers import (
    AvailabilitySerializer,
    CancellationSerializer,
    EventSerializer,
    ProductSerializer,
    ResortSerializer,
    TeamSerializer,
)


from formtools.wizard.views import SessionWizardView
from .forms import EventForm, TeamForm, AvailabilityForm

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

class CancellationViewSet(viewsets.ModelViewSet):
    queryset = Cancellation.objects.all()
    serializer_class = CancellationSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ResortViewSet(viewsets.ModelViewSet):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer


class EventListView(ListView):
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        return (
            Event.objects.select_related("resort")
            .prefetch_related("team__availabilities__profile")
            .order_by("start_date", "name")
        )


class EventDetailView(DetailView):
    template_name = "events/event_detail.html"
    context_object_name = "event"
    model = Event

    def get_queryset(self):
        return Event.objects.select_related("resort").prefetch_related(
            "team__availabilities__profile__user"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = getattr(self.object, "team", None)
        context["team"] = team
        if team:
            context["availabilities"] = team.availabilities.select_related(
                "profile", "profile__user"
            )
        else:
            context["availabilities"] = []
        return context


class EventCreateView(View):
    template_name = "events/event_form.html"

    def get(self, request):
        event_form = EventForm()
        team_form = TeamForm(prefix="team")
        return render(
            request,
            self.template_name,
            {"event_form": event_form, "team_form": team_form},
        )

    def post(self, request):
        event_form = EventForm(request.POST)
        team_form = TeamForm(request.POST, prefix="team")

        team_has_data = team_form.has_changed()

        if not event_form.is_valid() or (team_has_data and not team_form.is_valid()):
            return render(
                request,
                self.template_name,
                {"event_form": event_form, "team_form": team_form},
            )

        event = event_form.save()

        if team_has_data:
            team = team_form.save(commit=False)
            team.event = event
            team.save()

        return redirect("events:event_detail", pk=event.pk)


class TeamListView(ListView):
    template_name = "events/team_list.html"
    context_object_name = "teams"

    def get_queryset(self):
        return Team.objects.select_related("event").prefetch_related("availabilities__profile").order_by(
            "event__start_date", "name"
        )


class TeamDetailView(DetailView):
    template_name = "events/team_detail.html"
    context_object_name = "team"
    model = Team

    def get_queryset(self):
        return Team.objects.select_related("event").prefetch_related(
            "availabilities__profile", "availabilities__profile__user"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["availabilities"] = self.object.availabilities.select_related(
            "profile", "profile__user"
        )
        return context


class TeamStatusUpdateView(View):
    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        action = request.POST.get("action")
        if action == "close":
            team.status = True
        elif action == "open":
            team.status = False
        team.save()
        return redirect("events:team_detail", pk=pk)


class AvailabilityStatusUpdateView(View):
    def post(self, request, pk):
        availability = get_object_or_404(Availability, pk=pk)
        if "status" in request.POST:
            availability.status = request.POST.get("status") == "true"
        if "summoned" in request.POST:
            availability.summoned = request.POST.get("summoned") == "true"
        availability.save()
        return redirect("events:team_detail", pk=availability.team_id)


class EventWizard(SessionWizardView):
    template_name = "events/event_wizard.html"
    form_list = [EventForm, TeamForm, AvailabilityForm]

    def done(self, form_list, **kwargs):
        event_form = form_list[0]
        team_form = form_list[1]
        availability_form = form_list[2]

        event = event_form.save()
        team = team_form.save(commit=False)
        team.event = event
        team.save()

        availability = availability_form.save(commit=False)
        availability.team = team
        availability.save()

        return render(self.request, 'events/done.html', {
            'event': event,
            'team': team,
            'availability': availability
        })
