import json
import traceback

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET

from .models import Shipment, UserProfile


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def login_view(request):
    """Standard login page — CSRF-protected."""
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    error = None
    if request.method == "POST":
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        error = "Invalid email or password."

    return render(request, "shipments/login.html", {"error": error})


@login_required
def logout_view(request):
    logout(request)
    return redirect("/login/")


# ---------------------------------------------------------------------------
# Dashboard & Tracking
# ---------------------------------------------------------------------------

@login_required
def dashboard_view(request):
    """Main dashboard — shipment overview."""
    recent_shipments = Shipment.objects.select_related("customer").all()[:10]
    stats = {
        "total": Shipment.objects.count(),
        "in_transit": Shipment.objects.filter(status="in_transit").count(),
        "delivered": Shipment.objects.filter(status="delivered").count(),
        "pending": Shipment.objects.filter(status="pending").count(),
    }
    return render(
        request,
        "shipments/dashboard.html",
        {"shipments": recent_shipments, "stats": stats},
    )


@login_required
def tracking_view(request):
    """Package tracking search — this endpoint is SAFE (parameterised query)."""
    result = None
    query = request.GET.get("q", "").strip()
    not_found = False

    if query:
        result = (
            Shipment.objects.select_related("customer")
            .filter(tracking_number__iexact=query)
            .first()
        )
        if result is None:
            not_found = True

    return render(
        request,
        "shipments/tracking.html",
        {"result": result, "query": query, "not_found": not_found},
    )


@login_required
def shipment_history_view(request):
    """Full shipment history list."""
    shipments = Shipment.objects.select_related("customer").all()[:50]
    return render(
        request, "shipments/history.html", {"shipments": shipments}
    )


# ---------------------------------------------------------------------------
# Profile — VULN 1: CSRF + mass-assignment on role
# ---------------------------------------------------------------------------

@login_required
def profile_view(request):
    """Display profile page with update form."""
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user, defaults={"role": "user"}
    )
    return render(request, "shipments/profile.html", {"profile": profile})


@csrf_exempt
@login_required
@require_POST
def profile_update_view(request):
    """
    VULNERABLE: no CSRF protection (@csrf_exempt) and accepts `role` param
    from the request body (mass-assignment).
    """
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user, defaults={"role": "user"}
    )

    first_name = request.POST.get("first_name", request.user.first_name)
    last_name = request.POST.get("last_name", request.user.last_name)
    email = request.POST.get("email", request.user.email)
    phone = request.POST.get("phone", profile.phone)
    department = request.POST.get("department", profile.department)

    # Mass-assignment: role is accepted from client without authorization check
    role = request.POST.get("role", profile.role)

    request.user.first_name = first_name
    request.user.last_name = last_name
    request.user.email = email
    request.user.save()

    profile.phone = phone
    profile.department = department
    profile.role = role
    profile.save()

    return redirect("/profile/?updated=1")


# ---------------------------------------------------------------------------
# Admin panel — gated by role
# ---------------------------------------------------------------------------

@login_required
def admin_panel_view(request):
    """Returns 403 for non-admin users, 200 with admin panel for admins."""
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user, defaults={"role": "user"}
    )
    if profile.role != "admin":
        return HttpResponseForbidden(
            render(request, "shipments/403.html").content
        )
    shipments = Shipment.objects.select_related("customer").all()[:50]
    return render(request, "shipments/admin_panel.html", {"shipments": shipments})


# ---------------------------------------------------------------------------
# API — Shipment search — VULN 2: SQL injection
# ---------------------------------------------------------------------------

@login_required
@require_GET
def api_shipment_search(request):
    """
    VULNERABLE: raw SQL with string concatenation on `destination` parameter.
    PostgreSQL error messages are exposed in the response.
    """
    destination = request.GET.get("destination", "")

    if not destination:
        return JsonResponse({"error": "Missing 'destination' parameter."}, status=400)

    # INTENTIONALLY VULNERABLE — raw SQL concatenation
    sql = (
        "SELECT s.id, s.tracking_number, s.origin, s.destination, s.status, "
        "s.weight_kg, s.description, s.created_at, c.name AS customer_name "
        "FROM shipments_shipment s "
        "JOIN shipments_customer c ON s.customer_id = c.id "
        "WHERE s.destination ILIKE '%%"
        + destination
        + "%%' ORDER BY s.created_at DESC LIMIT 50"
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Serialize dates/decimals
        for row in rows:
            for key, value in row.items():
                if hasattr(value, "isoformat"):
                    row[key] = value.isoformat()
                elif hasattr(value, "__float__"):
                    row[key] = float(value)

        return JsonResponse({"results": rows, "count": len(rows)})

    except Exception as exc:
        # Expose PostgreSQL error details (intentionally verbose)
        return JsonResponse(
            {
                "error": "Database error",
                "detail": str(exc),
                "query": sql,
                "trace": traceback.format_exc(),
            },
            status=500,
        )


# ---------------------------------------------------------------------------
# Index redirect
# ---------------------------------------------------------------------------

def index_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    return redirect("/login/")
