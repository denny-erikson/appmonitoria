from django.urls import path
from .views import EventCreateView, EventDetailView, EventListView, EventWizard

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="event_list"),
    path("new/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path('event_wizard/', EventWizard.as_view(), name='event_wizard'),
]
