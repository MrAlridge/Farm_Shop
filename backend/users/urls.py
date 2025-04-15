# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SocialSupportViewSet, LoginView, PoorApplicationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'social_supports', SocialSupportViewSet, basename='social_support')
router.register(r'poor-applications', PoorApplicationViewSet, basename='poor-application')

urlpatterns = [
    path('login/', LoginView.as_view(), name='user-login'),
    path('', include(router.urls)),
]