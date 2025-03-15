# users/serializers.py
from rest_framework import serializers
from .models import User, SocialSupport

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