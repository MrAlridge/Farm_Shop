# fupin_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')), # 包含users应用的路由
    path('api/poverty/', include('poverty.urls')),  # 添加 poverty 应用的 URL
    path('api/products/', include('products.urls')),  # 添加 products 应用的 URL
    path('api/orders/', include('orders.urls')),  # 添加 orders 应用的 URL
]