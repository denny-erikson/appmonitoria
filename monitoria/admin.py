from django.contrib import admin
from .models import Address, BankAccount, Document, Location, Rating, Uniform, Payment, Category

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'event', 'score', 'score_display', 'created_by', 'created_at')
    list_filter = ('score', 'event', 'created_at')
    search_fields = ('profile__name', 'event__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('profile', 'event', 'created_by')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('profile', 'event', 'score', 'description')
        }),
        ('Metadados', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('created_by',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # if creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Registre cada modelo
admin.site.register(Location)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Document)
admin.site.register(Uniform)
admin.site.register(Payment)
admin.site.register(Category)
