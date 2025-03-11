from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

router = DefaultRouter() # 创建一个默认的路由
router.register(r'users', views.UserViewSet) # 注册用户相关的路由，URL路径为 /api/users/
router.register(r'poor_households', views.PoorHouseholdViewSet) # 注册贫困户信息相关的路由，URL路径为 /api/poor_households/
router.register(r'audit_records', views.AuditRecordViewSet)
router.register(r'assistance_connections', views.AssistanceConnectionViewSet)
router.register(r'material_assistances', views.MaterialAssistanceViewSet)
router.register(r'education_assistances', views.EducationAssistanceViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'logistics', views.LogisticsViewSet)
router.register(r'chat_messages', views.ChatMessageViewSet)


urlpatterns = [
    path('', include(router.urls)), # 将 router 中的路由包含进来
]