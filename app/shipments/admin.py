from django.contrib import admin
from .models import Customer, Shipment, UserProfile


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "created_at")
    search_fields = ("name", "email", "company")


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "customer", "origin", "destination", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("tracking_number", "destination", "origin")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "department")
    list_filter = ("role",)
