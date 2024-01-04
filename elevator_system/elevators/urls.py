# elevators/urls.py
from rest_framework import routers
from .views import ElevatorViewSet

router = routers.DefaultRouter()
router.register(r'elevators', ElevatorViewSet)

urlpatterns = router.urls
