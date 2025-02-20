from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render

from events.models import Availability, Cancellation, Event, Product, Resort, Team
from events.serializers import AvailabilitySerializer, CancellationSerializer, EventSerializer, ProductSerializer, ResortSerializer, TeamSerializer


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