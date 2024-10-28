from django.contrib import admin
from .models import Address, BankAccount, Document, Location, Uniform, Product, Event, Team, Resort, Availability, Cancellation, Payment

# Registre cada modelo
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Document)
admin.site.register(Uniform)
admin.site.register(Product)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(Resort)
admin.site.register(Availability)
admin.site.register(Cancellation)
admin.site.register(Payment)
