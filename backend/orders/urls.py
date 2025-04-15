# orders/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]