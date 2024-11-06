from rest_framework import viewsets
from .models import (
    Address, BankAccount, Category, Document, Location, Uniform, Payment
)
from .serializers import (
    AddressSerializer, BankAccountSerializer, CategorySerializer, DocumentsSerializer, LocationSerializer,
    UniformSerializer, PaymentSerializer
)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentsSerializer

class UniformViewSet(viewsets.ModelViewSet):
    queryset = Uniform.objects.all()
    serializer_class = UniformSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
