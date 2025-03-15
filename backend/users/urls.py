# users/urls.py
from django.urls import path, include
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'social_supports',views.SocialSupportViewSet)

urlpatterns = [
     path('', include(router.urls)),
]