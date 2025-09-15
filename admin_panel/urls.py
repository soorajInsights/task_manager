from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admins/", views.admins_list, name="admins_list"),
    path("admins/create/", views.create_admin, name="create_admin"),
]
