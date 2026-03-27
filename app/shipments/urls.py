from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("tracking/", views.tracking_view, name="tracking"),
    path("history/", views.shipment_history_view, name="history"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update", views.profile_update_view, name="profile_update"),
    path("admin/", views.admin_panel_view, name="admin_panel"),
    path("api/shipments/search", views.api_shipment_search, name="api_shipment_search"),
]
