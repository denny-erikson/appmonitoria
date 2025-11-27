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
