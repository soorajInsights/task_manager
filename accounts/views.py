from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import UserSerializer

class AdminViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Simple API to list Admins and SuperAdmins
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(role__in=["ADMIN", "SUPERADMIN"])
