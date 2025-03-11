from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')), # 将 backend.urls 包含到 api/ 路径下
]