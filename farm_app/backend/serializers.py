from rest_framework import serializers
from backend.models import User, PoorHousehold, AuditRecord, AssistanceConnection, MaterialAssistance, EducationAssistance, Product, Order, Logistics, ChatMessage

# 用户 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'user_type', 'email', 'first_name', 'last_name'] # 包含需要序列化的字段
        extra_kwargs = {'password': {'write_only': True}} # password 字段只用于写入，不进行序列化输出

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # 使用 create_user 创建用户，密码会被自动哈希
        return user

# 贫困户信息 Serializer
class PoorHouseholdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # 嵌套用户 Serializer，只读

    class Meta:
        model = PoorHousehold
        fields = '__all__' # 序列化所有字段
        read_only_fields = ['application_status'] # 申请状态字段只读，由后端控制

# 贫困户审核记录 Serializer
class AuditRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditRecord
        fields = '__all__'

# 帮扶对接 Serializer
class AssistanceConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistanceConnection
        fields = '__all__'

# 物资援助 Serializer
class MaterialAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialAssistance
        fields = '__all__'

# 教育资助 Serializer
class EducationAssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationAssistance
        fields = '__all__'

# 商品 Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# 订单 Serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# 物流跟踪 Serializer
class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistics
        fields = '__all__'

# 客服消息 Serializer
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'