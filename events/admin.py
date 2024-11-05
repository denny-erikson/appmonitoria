from django.contrib import admin

from events.models import Availability, Cancellation, Event, Product, Resort, Team

# Register your models here.
admin.site.register(Product)
admin.site.register(Resort)

class TeamInline(admin.StackedInline):
    model = Team
    extra = 0 

class EventAdmin(admin.ModelAdmin):
    inlines = [TeamInline]

admin.site.register(Event, EventAdmin)

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 0

class TeamAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInline]

admin.site.register(Team, TeamAdmin)

class CancellationInline(admin.TabularInline):
    model = Cancellation
    extra = 0  # Não exibe formulários vazios adicionais

class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('profile', 'status', 'summoned', 'team')
    inlines = [CancellationInline]

admin.site.register(Availability, AvailabilityAdmin)

class CancellationAdmin(admin.ModelAdmin):
    list_display = ('reason', 'availability')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.availability:
            obj.availability.cancel(obj.reason)

admin.site.register(Cancellation, CancellationAdmin)