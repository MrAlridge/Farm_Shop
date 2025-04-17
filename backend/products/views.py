from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter  # 需要自定义的过滤器
from rest_framework import status

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter  # 用于筛选的过滤器类
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sales', 'created_at']
    permission_classes = [permissions.IsAuthenticated]  # 添加权限要求
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'upload_image']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def filter_products(self, request):
        # 获取前端传递的筛选条件
        min_price = request.query_params.get('min_price', 0)
        max_price = request.query_params.get('max_price', 1000)
        category = request.query_params.get('category', '')
        sort_by = request.query_params.get('sort_by', 'price_asc')

        # 基于筛选条件进行查询
        products = Product.objects.filter(price__gte=min_price, price__lte=max_price)

        if category:
            products = products.filter(category__name=category)

        # 根据排序方式进行排序
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'sales_desc':
            products = products.order_by('-sales')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')

        # 分页
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='upload_image')
    def upload_image(self, request):
        """
        上传商品图片
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
        product_id = request.data.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(id=product_id, added_by=request.user)
                product.image = image
                product.save()
                
                # 返回图片URL
                request = self.request
                image_url = request.build_absolute_uri(product.image.url)
                return Response({
                    "message": "图片上传成功",
                    "url": image_url
                })
            except Product.DoesNotExist:
                return Response(
                    {"detail": "商品不存在或您没有权限修改该商品"},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # 如果没有提供商品ID，则只返回图片URL
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            from django.utils import timezone
            
            # 生成文件名
            file_name = f"temp_{request.user.id}_{int(timezone.now().timestamp())}{os.path.splitext(image.name)[1]}"
            
            # 保存文件
            path = default_storage.save(f'products/{file_name}', ContentFile(image.read()))
            
            # 返回图片URL
            request = self.request
            image_url = request.build_absolute_uri(default_storage.url(path))
            
            return Response({
                "message": "图片上传成功",
                "url": image_url,
                "path": path
            })

class CategoryViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def list_categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
