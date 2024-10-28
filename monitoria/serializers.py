from rest_framework import serializers
from .models import (
    Address, BankAccount, Document, Location, Uniform, Product,
    Event, Team, Resort, Availability, Cancellation, Payment
)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class DocumentsSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Document
        fields = '__all__'

class UniformSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Uniform
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Product
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Event
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Team
        fields = '__all__'

class ResortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resort
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Availability
        fields = '__all__'

class CancellationSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Cancellation
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
