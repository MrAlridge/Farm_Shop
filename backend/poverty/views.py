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
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'supporter']
    search_fields = ['name', 'description', 'content', 'contact_person']
    ordering_fields = ['created_at', 'start_date', 'end_date', 'deadline']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        根据不同的操作返回不同的权限类
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'upload_image']:
            permission_classes = [IsSocialUser]  # 只有社会帮扶人员可以创建和修改
        else:
            permission_classes = [IsAuthenticated]  # 其他操作需要登录
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        根据用户类型返回不同的查询集
        """
        user = self.request.user
        queryset = AssistanceRecord.objects.all()

        # 添加状态过滤
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        # 添加日期范围过滤
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        if user.is_staff:
            return queryset
        elif user.user_type == 'social':
            return queryset.filter(supporter=user)
        else:
            return queryset.filter(status='published')

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        发布项目
        """
        project = self.get_object()
        if project.supporter != request.user:
            return Response(
                {"detail": "只有项目创建者可以发布项目"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if project.status != 'draft':
            return Response(
                {"detail": "只有草稿状态的项目可以发布"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        project.status = 'published'
        project.save()
        return Response({"status": "项目已发布"})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        结束项目
        """
        project = self.get_object()
        if project.supporter != request.user:
            return Response(
                {"detail": "只有项目创建者可以结束项目"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if project.status != 'published':
            return Response(
                {"detail": "只有已发布状态的项目可以结束"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        project.status = 'closed'
        project.save()
        return Response({"status": "项目已结束"})

    @action(detail=False, methods=['get'])
    def my_projects(self, request):
        """
        获取当前用户的项目列表
        """
        if request.user.user_type != 'social':
            return Response(
                {"detail": "只有社会帮扶人员可以查看自己的项目"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        projects = self.get_queryset().filter(supporter=request.user)
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published_projects(self, request):
        """
        获取所有已发布的项目
        """
        projects = self.get_queryset().filter(status='published')
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['post'], url_path='upload-image')
    def upload_image(self, request):
        """
        上传项目图片
        """
        if 'image' not in request.FILES:
            return Response(
                {"detail": "请提供图片文件"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        image = request.FILES['image']
        
        # 验证文件类型
        if not image.content_type.startswith('image/'):
            return Response(
                {"detail": "只能上传图片文件"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 验证文件大小（限制为2MB）
        if image.size > 2 * 1024 * 1024:
            return Response(
                {"detail": "图片大小不能超过2MB"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 保存图片
        project_id = request.data.get('project_id')
        if project_id:
            try:
                project = AssistanceRecord.objects.get(id=project_id, supporter=request.user)
                project.image = image
                project.save()
                
                # 返回图片URL
                request = self.request
                image_url = request.build_absolute_uri(project.image.url)
                return Response({
                    "message": "图片上传成功",
                    "url": image_url
                })
            except AssistanceRecord.DoesNotExist:
                return Response(
                    {"detail": "项目不存在或您没有权限修改该项目"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # 如果没有提供项目ID，则只返回图片URL
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            
            # 生成文件名
            file_name = f"temp_{request.user.id}_{int(timezone.now().timestamp())}{os.path.splitext(image.name)[1]}"
            
            # 保存文件
            path = default_storage.save(f'assistance_images/{file_name}', ContentFile(image.read()))
            
            # 返回图片URL
            request = self.request
            image_url = request.build_absolute_uri(default_storage.url(path))
            
            return Response({
                "message": "图片上传成功",
                "url": image_url,
                "path": path
            })