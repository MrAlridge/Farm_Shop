# poverty/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'applications', views.PovertyApplicationViewSet)
router.register(r'records', views.AssistanceRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]