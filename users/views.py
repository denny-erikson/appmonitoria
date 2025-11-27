from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, render
from .models import CustomUser, Profile, Role
from .serializers import RoleSerializer, UserSerializer, ProfileSerializer
from .forms import UserProfileForm

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


# Frontend pages
class UserListView(ListView):
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return CustomUser.objects.prefetch_related("roles", "profile").order_by("username")


class UserDetailView(DetailView):
    template_name = "users/user_detail.html"
    context_object_name = "user_obj"
    model = CustomUser

    def get_queryset(self):
        return CustomUser.objects.prefetch_related("roles", "profile__category")


class UserProfileEditView(View):
    template_name = "users/user_profile_form.html"

    def get(self, request, pk=None):
        instance = None
        if pk:
            instance = get_object_or_404(CustomUser, pk=pk)
        form = UserProfileForm(instance=instance)
        return render(request, self.template_name, {"form": form, "user_obj": instance})

    def post(self, request, pk=None):
        instance = None
        if pk:
            instance = get_object_or_404(CustomUser, pk=pk)
        form = UserProfileForm(request.POST, instance=instance)
        if form.is_valid():
            user = form.save()
            return redirect("userpages:user_detail", pk=user.pk)
        return render(request, self.template_name, {"form": form, "user_obj": instance})
