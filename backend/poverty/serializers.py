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
    supporter = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = AssistanceRecord
        fields = [
            'id', 'name', 'image', 'image_url', 'description', 'content',
            'start_date', 'end_date', 'deadline',
            'contact_person', 'contact_phone', 'contact_email',
            'created_at', 'updated_at', 'supporter', 'status', 'status_display'
        ]
        read_only_fields = ['supporter', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

    def validate(self, data):
        """
        验证日期字段
        """
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("结束日期不能早于开始日期")
        
        if data.get('deadline') and data.get('start_date'):
            if data['deadline'] > data['start_date']:
                raise serializers.ValidationError("报名截止日期不能晚于项目开始日期")
        
        return data

    def validate_contact_phone(self, value):
        """
        验证手机号格式
        """
        if value and not value.isdigit():
            raise serializers.ValidationError("联系电话必须是数字")
        if value and len(value) != 11:
            raise serializers.ValidationError("联系电话必须是11位数字")
        return value

    def create(self, validated_data):
        """
        创建时自动设置supporter为当前用户
        """
        validated_data['supporter'] = self.context['request'].user
        return super().create(validated_data)