from django.contrib import admin
from .models import Address, BankAccount, Document, Location, Uniform, Product, Event, Team, Resort, Availability, Cancellation, Payment

# Registre cada modelo
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Document)
admin.site.register(Uniform)
admin.site.register(Product)
admin.site.register(Resort)
admin.site.register(Payment)
admin.site.register(Cancellation)

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