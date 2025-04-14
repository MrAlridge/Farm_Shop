# fupin_project/urls.py
from django.contrib import admin
from django.urls import path, include
# 获取CSRF TOKEN 视图
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')), # 包含users应用的路由
    path('api/poverty/', include('poverty.urls')),  # 添加 poverty 应用的 URL
    path('api/products/', include('products.urls')),  # 添加 products 应用的 URL
    path('api/orders/', include('orders.urls')),  # 添加 orders 应用的 URL
]