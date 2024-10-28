from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Role

class CustomUserAdmin(UserAdmin):
    # Exibir o campo 'Role' no admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('roles',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Role)
