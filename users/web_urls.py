from django.urls import path
from .views import UserListView, UserDetailView, UserProfileEditView

app_name = "userpages"

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("<uuid:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("new/", UserProfileEditView.as_view(), name="user_create"),
    path("<uuid:pk>/edit/", UserProfileEditView.as_view(), name="user_edit"),
]
