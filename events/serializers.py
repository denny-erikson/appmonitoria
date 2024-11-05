from events.models import Availability, Cancellation, Event, Product, Resort, Team
from rest_framework import serializers


class EventSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Event
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Team
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Availability
        fields = '__all__'

class CancellationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Cancellation
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = '__all__'


class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = '__all__'