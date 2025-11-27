from django.urls import path
from .views import (
    AvailabilityStatusUpdateView,
    EventCreateView,
    EventDetailView,
    EventListView,
    EventWizard,
    TeamAvailabilityCreateView,
    EventPaymentReportView,
    TeamDetailView,
    TeamListView,
    TeamStatusUpdateView,
    SelfAvailabilityView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("new/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("teams/", TeamListView.as_view(), name="team_list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team_detail"),
    path("teams/<int:pk>/availability/new/", TeamAvailabilityCreateView.as_view(), name="team_availability_create"),
    path("teams/<int:pk>/status/", TeamStatusUpdateView.as_view(), name="team_status_update"),
    path(
        "availability/<int:pk>/update/",
        AvailabilityStatusUpdateView.as_view(),
        name="availability_status_update",
    ),
    path("<int:pk>/payments/report/", EventPaymentReportView.as_view(), name="event_payment_report"),
    path("<int:event_pk>/availability/self/", SelfAvailabilityView.as_view(), name="self_availability"),
    path('event_wizard/', EventWizard.as_view(), name='event_wizard'),
]
