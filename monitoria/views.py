from rest_framework import viewsets
from .models import (
    Address,
    BankAccount,
    Category,
    Document,
    Location,
    Uniform,
    Payment,
    Rating,
)
from .serializers import (
    AddressSerializer,
    BankAccountSerializer,
    CategorySerializer,
    DocumentsSerializer,
    LocationSerializer,
    UniformSerializer,
    PaymentSerializer,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy

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


def teste(request):
    return render(request, "monitoria/teste.html")


# Frontend pages (HTML)
class PaymentListView(ListView):
    template_name = "monitoria/payment_list.html"
    context_object_name = "payments"

    def get_queryset(self):
        return Payment.objects.select_related("event", "profile", "profile__user").order_by(
            "-id"
        )


class PaymentDetailView(DetailView):
    template_name = "monitoria/payment_detail.html"
    context_object_name = "payment"
    model = Payment

    def get_queryset(self):
        return Payment.objects.select_related("event", "profile", "profile__user")

    def get_context_data(self, **kwargs):
        from .forms import PaymentStatusForm

        context = super().get_context_data(**kwargs)
        context["status_form"] = PaymentStatusForm(instance=self.object)
        return context


class PaymentStatusUpdateView(View):
    def post(self, request, pk):
        from .forms import PaymentStatusForm

        payment = get_object_or_404(Payment, pk=pk)
        form = PaymentStatusForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
        return redirect("monitoria:payment_detail", pk=pk)


class BankAccountListView(ListView):
    template_name = "monitoria/bankaccount_list.html"
    context_object_name = "bankaccounts"

    def get_queryset(self):
        return BankAccount.objects.select_related("user").order_by("bank_name")


class BankAccountDetailView(DetailView):
    template_name = "monitoria/bankaccount_detail.html"
    context_object_name = "bankaccount"
    model = BankAccount

    def get_queryset(self):
        return BankAccount.objects.select_related("user")


class BankAccountCreateView(CreateView):
    template_name = "monitoria/bankaccount_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:bankaccount_list")

    def get_form_class(self):
        from .forms import BankAccountForm
        return BankAccountForm


class BankAccountUpdateView(UpdateView):
    template_name = "monitoria/bankaccount_form.html"
    form_class = None
    model = BankAccount
    success_url = reverse_lazy("monitoria:bankaccount_list")
    context_object_name = "bankaccount"

    def get_form_class(self):
        from .forms import BankAccountForm
        return BankAccountForm


class AddressListView(ListView):
    template_name = "monitoria/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        return Address.objects.select_related("user", "location").order_by("user__username")


class AddressDetailView(DetailView):
    template_name = "monitoria/address_detail.html"
    context_object_name = "address"
    model = Address

    def get_queryset(self):
        return Address.objects.select_related("user", "location")


class AddressCreateView(CreateView):
    template_name = "monitoria/address_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:address_list")

    def get_form_class(self):
        from .forms import AddressForm
        return AddressForm


class AddressUpdateView(UpdateView):
    template_name = "monitoria/address_form.html"
    form_class = None
    model = Address
    success_url = reverse_lazy("monitoria:address_list")
    context_object_name = "address"

    def get_form_class(self):
        from .forms import AddressForm
        return AddressForm


class LocationListView(ListView):
    template_name = "monitoria/location_list.html"
    context_object_name = "locations"

    def get_queryset(self):
        return Location.objects.all().order_by("country", "state", "city")


class LocationDetailView(DetailView):
    template_name = "monitoria/location_detail.html"
    context_object_name = "location"
    model = Location


class LocationCreateView(CreateView):
    template_name = "monitoria/location_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:location_list")

    def get_form_class(self):
        from .forms import LocationForm
        return LocationForm


class LocationUpdateView(UpdateView):
    template_name = "monitoria/location_form.html"
    form_class = None
    model = Location
    success_url = reverse_lazy("monitoria:location_list")
    context_object_name = "location"

    def get_form_class(self):
        from .forms import LocationForm
        return LocationForm


class UniformListView(ListView):
    template_name = "monitoria/uniform_list.html"
    context_object_name = "uniforms"

    def get_queryset(self):
        return Uniform.objects.select_related("user").order_by("user__username")


class UniformDetailView(DetailView):
    template_name = "monitoria/uniform_detail.html"
    context_object_name = "uniform"
    model = Uniform

    def get_queryset(self):
        return Uniform.objects.select_related("user")


class UniformCreateView(CreateView):
    template_name = "monitoria/uniform_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:uniform_list")

    def get_form_class(self):
        from .forms import UniformForm
        return UniformForm


class UniformUpdateView(UpdateView):
    template_name = "monitoria/uniform_form.html"
    form_class = None
    model = Uniform
    success_url = reverse_lazy("monitoria:uniform_list")
    context_object_name = "uniform"

    def get_form_class(self):
        from .forms import UniformForm
        return UniformForm


class DocumentListView(ListView):
    template_name = "monitoria/document_list.html"
    context_object_name = "documents"

    def get_queryset(self):
        return Document.objects.select_related("user").order_by("user__username")


class DocumentDetailView(DetailView):
    template_name = "monitoria/document_detail.html"
    context_object_name = "document"
    model = Document

    def get_queryset(self):
        return Document.objects.select_related("user")


class DocumentCreateView(CreateView):
    template_name = "monitoria/document_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:document_list")

    def get_form_class(self):
        from .forms import DocumentForm
        return DocumentForm


class DocumentUpdateView(UpdateView):
    template_name = "monitoria/document_form.html"
    form_class = None
    model = Document
    success_url = reverse_lazy("monitoria:document_list")
    context_object_name = "document"

    def get_form_class(self):
        from .forms import DocumentForm
        return DocumentForm


class RatingListView(ListView):
    template_name = "monitoria/rating_list.html"
    context_object_name = "ratings"

    def get_queryset(self):
        return Rating.objects.select_related("event", "profile", "profile__user", "created_by").order_by(
            "-created_at"
        )


class RatingCreateView(CreateView):
    template_name = "monitoria/rating_form.html"
    form_class = None  # set in get_form_class to avoid circular import on load
    success_url = reverse_lazy("monitoria:rating_list")

    def get_form_class(self):
        from .forms import RatingForm
        return RatingForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class RatingUpdateView(UpdateView):
    template_name = "monitoria/rating_form.html"
    form_class = None
    model = Rating
    success_url = reverse_lazy("monitoria:rating_list")
    context_object_name = "rating"

    def get_form_class(self):
        from .forms import RatingForm
        return RatingForm


class CategoryListView(ListView):
    template_name = "monitoria/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all().order_by("title")


class CategoryCreateView(CreateView):
    template_name = "monitoria/category_form.html"
    form_class = None
    success_url = reverse_lazy("monitoria:category_list")

    def get_form_class(self):
        from .forms import CategoryForm
        return CategoryForm


class CategoryUpdateView(UpdateView):
    template_name = "monitoria/category_form.html"
    form_class = None
    model = Category
    success_url = reverse_lazy("monitoria:category_list")
    context_object_name = "category"

    def get_form_class(self):
        from .forms import CategoryForm
        return CategoryForm
