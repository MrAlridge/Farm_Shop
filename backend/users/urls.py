# users/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, SocialSupportViewSet, LoginView
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'social_supports', SocialSupportViewSet, basename='social_support')

urlpatterns = [
     path('login/', LoginView.as_view(), name='user-login'),
     path('', include(router.urls)),
]