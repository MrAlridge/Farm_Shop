# poverty/views.py
from rest_framework import viewsets, status
from .models import PovertyApplication, AssistanceRecord
from .serializers import PovertyApplicationSerializer, AssistanceRecordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class PovertyApplicationViewSet(viewsets.ModelViewSet):
    queryset = PovertyApplication.objects.all()
    serializer_class = PovertyApplicationSerializer

    def get_permissions(self):
      if self.action == 'create':
          permission_classes = [IsAuthenticated]  # 登录用户可以创建申请
      elif self.action == 'list':
          permission_classes = [IsAdminUser]
      else:
            permission_classes = [IsAuthenticated]
      return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        管理员可以查看所有申请,普通用户只能查看自己的申请
        """
        if self.request.user.is_staff:
            return PovertyApplication.objects.all()
        return PovertyApplication.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        application = self.get_object()
        application.status = 'approved'
        application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = 'rejected'
        application.save()
        serializer = self.get_serializer(application)
        return Response(serializer.data)

    # def perform_create(self, serializer):  # 在序列化器中处理创建逻辑,此处不需要
    #   serializer.save(user=self.request.user)
class AssistanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AssistanceRecord.objects.all()
    serializer_class = AssistanceRecordSerializer

    def get_permissions(self):
      if self.action == 'create':
          permission_classes = [IsAuthenticated]  # 登录用户可以创建申请
      elif self.action == 'list':
            permission_classes = [IsAuthenticated]
      else:
            permission_classes = [IsAuthenticated]
      return [permission() for permission in permission_classes]
    def get_queryset(self):
        """
        管理员可以查看所有援助记录,用户只能查看自己的
        """
        user = self.request.user
        if user.is_staff:
            return AssistanceRecord.objects.all()
        elif user.user_type == 'social':
            return AssistanceRecord.objects.filter(supporter=user)
        else :
            return AssistanceRecord.objects.filter(application__user=user)

    # def perform_create(self, serializer):  #在序列化器中处理创建逻辑
    #     serializer.save(supporter=self.request.user)