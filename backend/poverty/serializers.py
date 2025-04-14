# poverty/serializers.py
from rest_framework import serializers
from .models import PovertyApplication, AssistanceRecord
from users.serializers import UserSerializer  # 确保正确导入 UserSerializer

class PovertyApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 使用 UserSerializer
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PovertyApplication
        fields = [
            'id', 'user', 'title', 'content', 'status', 'status_display',
            'created_at', 'reviewed_at', 'review_comment', 'username'
        ]
        read_only_fields = [
            'user',  # user 字段设为只读，由后端自动设置
            'status', 
            'reviewed_at', 
            'review_comment'
        ]

    def create(self, validated_data):
        """
        创建申请时自动设置用户
        """
        user = self.context['request'].user
        validated_data['user'] = user
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