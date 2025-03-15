# users/views.py
from rest_framework import viewsets
from .models import User, SocialSupport
from .serializers import UserSerializer, SocialSupportSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
class UserViewSet(viewsets.ModelViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     def get_permissions(self):
        """
        重写get_permissions方法,允许任何人创建用户，但只有管理员可以查看用户列表,用户自己可以查看、修改
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
     def retrieve(self, request, pk=None):
        """
        重写retrieve方法,用户可以查看自己的信息，管理员可以查看所有用户信息
        """
        if request.user.is_staff or str(request.user.pk) == pk:
            user = self.get_object()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"detail": "您没有权限查看此用户信息。"}, status=403)

class SocialSupportViewSet(viewsets.ModelViewSet):
    queryset = SocialSupport.objects.all()
    serializer_class = SocialSupportSerializer

    def get_queryset(self):
        """
        重写get_queryset,只返回当前用户
        """
        return SocialSupport.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        """
        重写perform_create,自动关联到当前用户
        """
        serializer.save(user=self.request.user)