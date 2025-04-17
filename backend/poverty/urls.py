# poverty/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PovertyApplicationViewSet, AssistanceRecordViewSet

router = DefaultRouter()
router.register(r'applications', PovertyApplicationViewSet)
router.register(r'projects', AssistanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]