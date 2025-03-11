from rest_framework import viewsets
from backend.models import User, PoorHousehold, AuditRecord, AssistanceConnection, MaterialAssistance, EducationAssistance, Product, Order, Logistics, ChatMessage
from backend.serializers import UserSerializer, PoorHouseholdSerializer, AuditRecordSerializer, AssistanceConnectionSerializer, MaterialAssistanceSerializer, EducationAssistanceSerializer, ProductSerializer, OrderSerializer, LogisticsSerializer, ChatMessageSerializer

# 用户 ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 贫困户信息 ViewSet
class PoorHouseholdViewSet(viewsets.ModelViewSet):
    queryset = PoorHousehold.objects.all()
    serializer_class = PoorHouseholdSerializer

# 贫困户审核记录 ViewSet
class AuditRecordViewSet(viewsets.ModelViewSet):
    queryset = AuditRecord.objects.all()
    serializer_class = AuditRecordSerializer

# 帮扶对接 ViewSet
class AssistanceConnectionViewSet(viewsets.ModelViewSet):
    queryset = AssistanceConnection.objects.all()
    serializer_class = AssistanceConnectionSerializer

# 物资援助 ViewSet
class MaterialAssistanceViewSet(viewsets.ModelViewSet):
    queryset = MaterialAssistance.objects.all()
    serializer_class = MaterialAssistanceSerializer

# 教育资助 ViewSet
class EducationAssistanceViewSet(viewsets.ModelViewSet):
    queryset = EducationAssistance.objects.all()
    serializer_class = EducationAssistanceSerializer

# 商品 ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# 订单 ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# 物流跟踪 ViewSet
class LogisticsViewSet(viewsets.ModelViewSet):
    queryset = Logistics.objects.all()
    serializer_class = LogisticsSerializer

# 客服消息 ViewSet
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer