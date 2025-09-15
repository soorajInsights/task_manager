from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .forms import CreateAdminForm

# Decorators
def staff_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("admin_panel:login")
        if request.user.role not in ("ADMIN", "SUPERADMIN"):
            messages.error(request, "Permission denied.")
            return redirect("admin_panel:login")
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped

def superadmin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "SUPERADMIN":
            messages.error(request, "Only SuperAdmin allowed.")
            return redirect("admin_panel:dashboard")
        return view_func(request, *args, **kwargs)
    _wrapped.__name__ = view_func.__name__
    return _wrapped

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("admin_panel:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "admin_panel/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("admin_panel:login")

@staff_required
def dashboard(request):
    counts = {
        "total_admins": CustomUser.objects.filter(role="ADMIN").count(),
        "total_superadmins": CustomUser.objects.filter(role="SUPERADMIN").count(),
    }
    return render(request, "admin_panel/dashboard.html", {"counts": counts})

@staff_required
def admins_list(request):
    # Show all admins and superadmins
    admins = CustomUser.objects.exclude(is_superuser=False).filter(role__in=["ADMIN","SUPERADMIN"])
    # but simpler: show only users with role ADMIN or SUPERADMIN
    admins = CustomUser.objects.filter(role__in=["ADMIN","SUPERADMIN"])
    return render(request, "admin_panel/admins_list.html", {"admins": admins})

@staff_required
@superadmin_required
def create_admin(request):
    # Only SuperAdmin can create other SuperAdmin/ADMIN users through this view
    if request.method == "POST":
        form = CreateAdminForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            # Ensure role is one of allowed values; allow SuperAdmin to choose role
            if admin.role not in ("ADMIN", "SUPERADMIN"):
                admin.role = "ADMIN"
            admin.save()
            messages.success(request, "Admin created successfully.")
            return redirect("admin_panel:admins_list")
    else:
        form = CreateAdminForm(initial={"role": "ADMIN"})
    return render(request, "admin_panel/create_admin.html", {"form": form})
