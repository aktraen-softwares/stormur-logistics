from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shipments_customer"

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
        ("cancelled", "Cancelled"),
    ]

    tracking_number = models.CharField(max_length=20, unique=True, db_index=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="shipments"
    )
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    weight_kg = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "shipments_shipment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tracking_number} - {self.destination}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Administrator"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "shipments_userprofile"

    def __str__(self):
        return f"{self.user.username} ({self.role})"
