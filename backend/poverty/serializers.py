# poverty/serializers.py
from rest_framework import serializers
from .models import PovertyApplication, AssistanceRecord
from users.serializers import UserSerializer  # 确保正确导入 UserSerializer

class PovertyApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 使用 UserSerializer
    status = serializers.CharField(read_only=True)
    class Meta:
        model = PovertyApplication
        fields = '__all__'
    def create(self, validated_data):
        # 自动设置申请用户为当前请求用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AssistanceRecordSerializer(serializers.ModelSerializer):
    application = PovertyApplicationSerializer(read_only = True)
    supporter = UserSerializer(read_only=True)

    class Meta:
        model = AssistanceRecord
        fields = '__all__'
    def create(self, validated_data):
        # 自动设置申请用户为当前请求用户
        validated_data['supporter'] = self.context['request'].user
        return super().create(validated_data)