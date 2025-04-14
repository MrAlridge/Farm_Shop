# poverty/views.py
from rest_framework import viewsets, status
from .models import PovertyApplication, AssistanceRecord
from .serializers import PovertyApplicationSerializer, AssistanceRecordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .permissions import IsSocialUser, IsOwnerOrAdmin
from django.utils import timezone

class PovertyApplicationViewSet(viewsets.ModelViewSet):
    queryset = PovertyApplication.objects.all()
    serializer_class = PovertyApplicationSerializer

    def get_permissions(self):
        """
        根据不同的操作返回不同的权限类
        """
        if self.action == 'create':
            # 只有普通用户可以创建申请
            permission_classes = [IsSocialUser]
        elif self.action == 'list':
            # 已认证的用户可以获取列表（管理员获取所有，普通用户获取自己的）
            permission_classes = [IsAuthenticated]
        elif self.action in ['approve', 'reject']:
            # 只有管理员可以审批
            permission_classes = [IsAdminUser]
        else:
            # 其他操作需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        管理员可以查看所有申请，普通用户只能查看自己的申请
        """
        queryset = PovertyApplication.objects.all()
        if self.request.user.is_staff:
            return queryset.order_by('-created_at')
        return queryset.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        创建申请时自动关联当前用户
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        重写创建方法，添加额外的验证
        """
        # 检查用户是否已有待审核的申请
        if PovertyApplication.objects.filter(
            user=request.user,
            status='pending'
        ).exists():
            return Response(
                {'detail': '您已有待审核的申请，请等待审核完成后再提交新的申请'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        审批通过申请
        """
        application = self.get_object()
        if application.status != 'pending':
            return Response(
                {'detail': '只能审核待处理的申请'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.save()

        # 更新用户类型为贫困户
        user = application.user
        user.user_type = 'poor'
        user.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        拒绝申请
        """
        application = self.get_object()
        if application.status != 'pending':
            return Response(
                {'detail': '只能审核待处理的申请'},
                status=status.HTTP_400_BAD_REQUEST
            )

        review_comment = request.data.get('review_comment')
        if not review_comment:
            return Response(
                {'detail': '请提供拒绝原因'},
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = 'rejected'
        application.reviewed_at = timezone.now()
        application.review_comment = review_comment
        application.save()

        serializer = self.get_serializer(application)
        return Response(serializer.data)

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