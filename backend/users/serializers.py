# users/serializers.py
from rest_framework import serializers
from .models import User, SocialSupport, PoorApplication

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'user_type', 'phone_number', 'first_name', 'last_name', 'email')  # 根据需要选择字段,这里我为您添加了一些常用的字段
        extra_kwargs = {'password': {'write_only': True}} # 密码仅用于写入

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SocialSupportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SocialSupport
        fields = ('user', 'company_name', 'contact_person')

class PoorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoorApplication
        fields = ['id', 'reason', 'supporting_documents', 'status', 'created_at', 'reviewed_at', 'review_comment']
        read_only_fields = ['status', 'reviewed_at', 'review_comment']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)