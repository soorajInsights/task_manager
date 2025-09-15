from rest_framework.routers import DefaultRouter
from .views import AdminViewSet

router = DefaultRouter()
router.register(r"admins", AdminViewSet, basename="admins")

urlpatterns = router.urls
