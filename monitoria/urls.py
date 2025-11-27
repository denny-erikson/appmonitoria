from django.urls import path
from .views import (
    PaymentDetailView,
    PaymentListView,
    PaymentStatusUpdateView,
    RatingCreateView,
    RatingListView,
    RatingUpdateView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    DocumentListView,
    DocumentCreateView,
    DocumentDetailView,
    DocumentUpdateView,
    BankAccountListView,
    BankAccountCreateView,
    BankAccountDetailView,
    BankAccountUpdateView,
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
    path("ratings/", RatingListView.as_view(), name="rating_list"),
    path("ratings/new/", RatingCreateView.as_view(), name="rating_create"),
    path("ratings/<int:pk>/edit/", RatingUpdateView.as_view(), name="rating_edit"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/new/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_edit"),
    path("documents/", DocumentListView.as_view(), name="document_list"),
    path("documents/new/", DocumentCreateView.as_view(), name="document_create"),
    path("documents/<int:pk>/", DocumentDetailView.as_view(), name="document_detail"),
    path("documents/<int:pk>/edit/", DocumentUpdateView.as_view(), name="document_edit"),
    path("bankaccounts/", BankAccountListView.as_view(), name="bankaccount_list"),
    path("bankaccounts/new/", BankAccountCreateView.as_view(), name="bankaccount_create"),
    path("bankaccounts/<int:pk>/", BankAccountDetailView.as_view(), name="bankaccount_detail"),
    path("bankaccounts/<int:pk>/edit/", BankAccountUpdateView.as_view(), name="bankaccount_edit"),
]
