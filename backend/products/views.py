# products/views.py
from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category', 'name'] #基于分类和名称过滤
    search_fields = ['name', 'description'] #基于名称和描述搜索
    ordering_fields = ['price', 'created_at'] #基于价格和创建日期排序
    def get_permissions(self):
        if self.action == 'create':
          permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        管理员可以查看所有产品，用户只能查看自己添加的
        """
        if self.request.user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(added_by=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(added_by=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]