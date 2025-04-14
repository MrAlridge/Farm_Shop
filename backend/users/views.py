# users/views.py
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import User, SocialSupport, PoorApplication
from .serializers import UserSerializer, SocialSupportSerializer, PoorApplicationSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        """
        重写get_permissions方法,允许任何人创建用户，但只有管理员可以查看用户列表,用户自己可以查看、修改
        """
        if self.action == 'create':
            # 注意：注册操作在这里，权限是 AllowAny
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'me':  # 添加 me 动作的权限
            permission_classes = [IsAuthenticated]
        # retrieve, update, partial_update, destroy 需要认证
        else:
           permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def retrieve(self, request, pk=None):
        """
        重写retrieve方法,用户可以查看自己的信息，管理员可以查看所有用户信息
        """
        # 检查用户是否是管理员或者正在请求自己的信息
        if request.user.is_staff or (request.user.is_authenticated and str(request.user.pk) == pk):
             try:
                user = self.get_object() # get_object 会处理 pk 不存在的情况
                serializer = UserSerializer(user)
                return Response(serializer.data)
             except Http404:
                 return Response({"detail": "用户未找到。"}, status=status.HTTP_404_NOT_FOUND)
        else:
             # 如果未认证或者请求的不是自己的信息且不是管理员
             return Response({"detail": "需要认证或没有权限查看此用户信息。"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET'])
    def me(self, request):
        """
        获取当前登录用户的信息
        """
        if not request.user.is_authenticated:
            return Response(
                {"detail": "未认证的用户。"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class SocialSupportViewSet(viewsets.ModelViewSet):
    queryset = SocialSupport.objects.all()
    serializer_class = SocialSupportSerializer
    permission_classes = [IsAuthenticated]

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

class LoginView(APIView):
    """
    处理用户登录请求。
    允许任何用户访问此端点。
    """
    # 关键：明确设置权限为 AllowAny，覆盖任何全局设置
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': '请提供用户名和密码。'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'user_type': user.user_type,
                    'is_staff': user.is_staff,
                    **serializer.data
                }
            })
        else:
            return Response(
                {'error': '用户名或密码无效。'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

class PoorApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = PoorApplicationSerializer
    
    def get_queryset(self):
        return PoorApplication.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['POST'])
    def approve(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "没有权限进行此操作"}, status=status.HTTP_403_FORBIDDEN)
            
        application.status = 'approved'
        application.reviewed_at = timezone.now()
        application.save()
        
        # 更新用户类型
        application.user.user_type = 'poor'
        application.user.save()
        
        return Response({"detail": "申请已通过"})

    @action(detail=True, methods=['POST'])
    def reject(self, request, pk=None):
        application = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "没有权限进行此操作"}, status=status.HTTP_403_FORBIDDEN)
            
        application.status = 'rejected'
        application.reviewed_at = timezone.now()
        application.review_comment = request.data.get('review_comment', '')
        application.save()
        
        return Response({"detail": "申请已拒绝"})