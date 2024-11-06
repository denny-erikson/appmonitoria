from django.contrib import admin
from .models import Address, BankAccount, Document, Location, Uniform, Payment, Category

# Registre cada modelo
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Document)
admin.site.register(Uniform)
admin.site.register(Payment)
admin.site.register(Category)
