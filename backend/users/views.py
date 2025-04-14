# users/views.py
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import User, SocialSupport
from .serializers import UserSerializer, SocialSupportSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
            return Response({'error': '请提供用户名和密码。'}, status=status.HTTP_400_BAD_REQUEST)

        # 验证用户
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            # 验证成功，生成 JWT Tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # 准备响应数据
            serializer = UserSerializer(user) # 序列化用户信息
            response_data = {
                'refresh': str(refresh),
                'access': access_token,
                'user': serializer.data # 将用户信息包含在响应中
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            # 验证失败
            return Response({'error': '用户名或密码无效。'}, status=status.HTTP_401_UNAUTHORIZED)