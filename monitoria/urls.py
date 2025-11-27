from django.urls import path
from .views import (
    PaymentDetailView,
    PaymentListView,
    PaymentStatusUpdateView,
    teste,
)

app_name = "monitoria"

urlpatterns = [
    path("teste/", teste, name="teste"),
    path("payments/", PaymentListView.as_view(), name="payment_list"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment_detail"),
    path(
        "payments/<int:pk>/status/",
        PaymentStatusUpdateView.as_view(),
        name="payment_status_update",
    ),
]
