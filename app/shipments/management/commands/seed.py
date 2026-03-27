"""Seed database with initial data for the Stormur Logistics platform."""

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from shipments.models import Customer, Shipment, UserProfile


class Command(BaseCommand):
    help = "Seed the database with users, customers, and shipments."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # ------------------------------------------------------------------
        # Users
        # ------------------------------------------------------------------
        auditor, created = User.objects.get_or_create(
            username="auditor@stormur.is",
            defaults={
                "email": "auditor@stormur.is",
                "first_name": "Security",
                "last_name": "Auditor",
                "is_active": True,
            },
        )
        if created:
            auditor.set_password("ST!audit2026")
            auditor.save()
        UserProfile.objects.get_or_create(
            user=auditor,
            defaults={"role": "user", "department": "External Audit", "phone": "+354 555 0100"},
        )

        admin_user, created = User.objects.get_or_create(
            username="admin@stormur.is",
            defaults={
                "email": "admin@stormur.is",
                "first_name": "Bjorn",
                "last_name": "Magnusson",
                "is_active": True,
                "is_staff": True,
            },
        )
        if created:
            admin_user.set_password("Stormur!Adm1n#2026")
            admin_user.save()
        UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={"role": "admin", "department": "Operations", "phone": "+354 555 0001"},
        )

        ops_user, created = User.objects.get_or_create(
            username="ops@stormur.is",
            defaults={
                "email": "ops@stormur.is",
                "first_name": "Katrin",
                "last_name": "Sigurdsdottir",
                "is_active": True,
            },
        )
        if created:
            ops_user.set_password("Ops#Stormur2026")
            ops_user.save()
        UserProfile.objects.get_or_create(
            user=ops_user,
            defaults={"role": "user", "department": "Logistics", "phone": "+354 555 0042"},
        )

        self.stdout.write(self.style.SUCCESS("  Users created."))

        # ------------------------------------------------------------------
        # Customers
        # ------------------------------------------------------------------
        customers_data = [
            {"name": "Nordica Fisheries", "email": "shipping@nordica.is", "phone": "+354 600 1000", "company": "Nordica Fisheries ehf."},
            {"name": "Reykjavik Biotech", "email": "logistics@rvkbio.is", "phone": "+354 600 2000", "company": "Reykjavik Biotech hf."},
            {"name": "Glacier Exports", "email": "ops@glacierexports.is", "phone": "+354 600 3000", "company": "Glacier Exports ehf."},
            {"name": "Vatnajokull Energy", "email": "supply@vatnajokull.is", "phone": "+354 600 4000", "company": "Vatnajokull Energy hf."},
            {"name": "Blue Lagoon Retail", "email": "orders@blretail.is", "phone": "+354 600 5000", "company": "Blue Lagoon Retail ehf."},
            {"name": "HafnarTech", "email": "warehouse@hafnartech.is", "phone": "+354 600 6000", "company": "HafnarTech hf."},
            {"name": "Akureyri Metals", "email": "freight@akmetals.is", "phone": "+354 600 7000", "company": "Akureyri Metals ehf."},
            {"name": "Selfoss Dairy Co.", "email": "dispatch@selfossdairy.is", "phone": "+354 600 8000", "company": "Selfoss Dairy Co."},
        ]

        customers = []
        for cdata in customers_data:
            c, _ = Customer.objects.get_or_create(
                email=cdata["email"], defaults=cdata
            )
            customers.append(c)

        self.stdout.write(self.style.SUCCESS("  Customers created."))

        # ------------------------------------------------------------------
        # Shipments
        # ------------------------------------------------------------------
        today = date.today()
        shipments_data = [
            # Nordica Fisheries
            {"tracking_number": "STM-2026-00001", "customer": customers[0], "origin": "Reykjavik, Iceland", "destination": "London, United Kingdom", "status": "delivered", "weight_kg": 245.50, "description": "Fresh Atlantic cod — temperature-controlled", "estimated_delivery": today - timedelta(days=3)},
            {"tracking_number": "STM-2026-00002", "customer": customers[0], "origin": "Isafjordur, Iceland", "destination": "Copenhagen, Denmark", "status": "in_transit", "weight_kg": 180.00, "description": "Frozen haddock fillets", "estimated_delivery": today + timedelta(days=2)},
            # Reykjavik Biotech
            {"tracking_number": "STM-2026-00003", "customer": customers[1], "origin": "Reykjavik, Iceland", "destination": "Boston, United States", "status": "in_transit", "weight_kg": 12.30, "description": "Laboratory samples — hazmat class 6.2", "estimated_delivery": today + timedelta(days=5)},
            {"tracking_number": "STM-2026-00004", "customer": customers[1], "origin": "Reykjavik, Iceland", "destination": "Oslo, Norway", "status": "pending", "weight_kg": 8.75, "description": "Biotech reagents — keep refrigerated", "estimated_delivery": today + timedelta(days=4)},
            # Glacier Exports
            {"tracking_number": "STM-2026-00005", "customer": customers[2], "origin": "Vik, Iceland", "destination": "Hamburg, Germany", "status": "delivered", "weight_kg": 520.00, "description": "Volcanic rock aggregate — construction grade", "estimated_delivery": today - timedelta(days=7)},
            {"tracking_number": "STM-2026-00006", "customer": customers[2], "origin": "Egilsstadir, Iceland", "destination": "Rotterdam, Netherlands", "status": "in_transit", "weight_kg": 340.00, "description": "Pumice stone — industrial", "estimated_delivery": today + timedelta(days=3)},
            # Vatnajokull Energy
            {"tracking_number": "STM-2026-00007", "customer": customers[3], "origin": "Reykjavik, Iceland", "destination": "Stockholm, Sweden", "status": "pending", "weight_kg": 65.00, "description": "Geothermal sensor equipment", "estimated_delivery": today + timedelta(days=6)},
            {"tracking_number": "STM-2026-00008", "customer": customers[3], "origin": "Akureyri, Iceland", "destination": "Helsinki, Finland", "status": "delivered", "weight_kg": 42.80, "description": "Monitoring instruments", "estimated_delivery": today - timedelta(days=1)},
            # Blue Lagoon Retail
            {"tracking_number": "STM-2026-00009", "customer": customers[4], "origin": "Grindavik, Iceland", "destination": "Paris, France", "status": "in_transit", "weight_kg": 28.50, "description": "Skincare products — silica mud range", "estimated_delivery": today + timedelta(days=2)},
            {"tracking_number": "STM-2026-00010", "customer": customers[4], "origin": "Grindavik, Iceland", "destination": "Berlin, Germany", "status": "pending", "weight_kg": 31.20, "description": "Mineral bath salts — retail packaging", "estimated_delivery": today + timedelta(days=5)},
            # HafnarTech
            {"tracking_number": "STM-2026-00011", "customer": customers[5], "origin": "Hafnarfjordur, Iceland", "destination": "Dublin, Ireland", "status": "delivered", "weight_kg": 15.00, "description": "Electronic components — server boards", "estimated_delivery": today - timedelta(days=5)},
            {"tracking_number": "STM-2026-00012", "customer": customers[5], "origin": "Hafnarfjordur, Iceland", "destination": "Manchester, United Kingdom", "status": "returned", "weight_kg": 9.40, "description": "Networking equipment — RMA return", "estimated_delivery": None},
            # Akureyri Metals
            {"tracking_number": "STM-2026-00013", "customer": customers[6], "origin": "Akureyri, Iceland", "destination": "Gdansk, Poland", "status": "in_transit", "weight_kg": 1200.00, "description": "Aluminium ingots — industrial grade", "estimated_delivery": today + timedelta(days=8)},
            {"tracking_number": "STM-2026-00014", "customer": customers[6], "origin": "Akureyri, Iceland", "destination": "Antwerp, Belgium", "status": "cancelled", "weight_kg": 800.00, "description": "Silicon alloy — order cancelled by customer", "estimated_delivery": None},
            # Selfoss Dairy
            {"tracking_number": "STM-2026-00015", "customer": customers[7], "origin": "Selfoss, Iceland", "destination": "Edinburgh, United Kingdom", "status": "delivered", "weight_kg": 95.00, "description": "Skyr and dairy products — refrigerated", "estimated_delivery": today - timedelta(days=2)},
            {"tracking_number": "STM-2026-00016", "customer": customers[7], "origin": "Selfoss, Iceland", "destination": "Oslo, Norway", "status": "in_transit", "weight_kg": 110.50, "description": "Artisan cheese collection", "estimated_delivery": today + timedelta(days=1)},
            # Extra shipments for variety
            {"tracking_number": "STM-2026-00017", "customer": customers[0], "origin": "Reykjavik, Iceland", "destination": "New York, United States", "status": "pending", "weight_kg": 300.00, "description": "Premium seafood assortment", "estimated_delivery": today + timedelta(days=7)},
            {"tracking_number": "STM-2026-00018", "customer": customers[2], "origin": "Vik, Iceland", "destination": "Tokyo, Japan", "status": "in_transit", "weight_kg": 150.00, "description": "Lava stone tiles — decorative", "estimated_delivery": today + timedelta(days=12)},
            {"tracking_number": "STM-2026-00019", "customer": customers[3], "origin": "Reykjavik, Iceland", "destination": "Toronto, Canada", "status": "delivered", "weight_kg": 22.00, "description": "Geothermal heat pump controllers", "estimated_delivery": today - timedelta(days=4)},
            {"tracking_number": "STM-2026-00020", "customer": customers[5], "origin": "Hafnarfjordur, Iceland", "destination": "Singapore", "status": "in_transit", "weight_kg": 7.80, "description": "FPGA development boards", "estimated_delivery": today + timedelta(days=10)},
        ]

        for sdata in shipments_data:
            Shipment.objects.get_or_create(
                tracking_number=sdata["tracking_number"], defaults=sdata
            )

        self.stdout.write(self.style.SUCCESS("  Shipments created."))
        self.stdout.write(self.style.SUCCESS("Seeding complete."))
