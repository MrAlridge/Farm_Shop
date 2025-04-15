# poverty/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PovertyApplicationViewSet

router = DefaultRouter()
router.register(r'applications', PovertyApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]