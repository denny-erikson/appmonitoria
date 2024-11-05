from rest_framework import viewsets
from django.shortcuts import render

from events.models import Availability, Cancellation, Event, Product, Resort, Team
from events.serializers import AvailabilitySerializer, CancellationSerializer, EventSerializer, ProductSerializer, ResortSerializer, TeamSerializer


class EventViewSet(viewsets.ModelViewSet):
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