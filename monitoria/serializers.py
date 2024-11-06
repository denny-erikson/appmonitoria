from rest_framework import serializers
from .models import (
    Address, BankAccount, Category, Document, Location, Uniform, Payment
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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
