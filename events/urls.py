from django.urls import path
from .views import (
    AvailabilityStatusUpdateView,
    EventCreateView,
    EventDetailView,
    EventListView,
    EventWizard,
    EventPaymentReportView,
    TeamDetailView,
    TeamListView,
    TeamStatusUpdateView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("new/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("teams/", TeamListView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
    path("teams/<int:pk>/status/", TeamStatusUpdateView.as_view(), name="team_status_update"),
    path(
        "availability/<int:pk>/update/",
        AvailabilityStatusUpdateView.as_view(),
        name="availability_status_update",
    ),
    path("<int:pk>/payments/report/", EventPaymentReportView.as_view(), name="event_payment_report"),
    path('event_wizard/', EventWizard.as_view(), name='event_wizard'),
]
