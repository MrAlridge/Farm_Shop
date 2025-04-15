from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .filters import ProductFilter  # 需要自定义的过滤器

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter  # 用于筛选的过滤器类
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'sales', 'created_at']
    
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

class CategoryViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def list_categories(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
