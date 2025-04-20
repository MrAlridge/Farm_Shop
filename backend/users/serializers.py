# users/serializers.py
from rest_framework import serializers
from .models import User, SocialSupport, PoorApplication

class UserSerializer(serializers.ModelSerializer):
    family_members = serializers.SerializerMethodField()
    annual_income = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'user_type', 'phone_number', 'first_name', 'last_name', 'email', 'family_members', 'annual_income')
        extra_kwargs = {'password': {'write_only': True}} # 密码仅用于写入

    def get_family_members(self, obj):
        if obj.user_type == 'poor':
            # 获取用户最新的已通过的贫困户申请
            latest_application = obj.poverty_applications.filter(status='approved').order_by('-created_at').first()
            if latest_application:
                return latest_application.family_members
        return None

    def get_annual_income(self, obj):
        if obj.user_type == 'poor':
            # 获取用户最新的已通过的贫困户申请
            latest_application = obj.poverty_applications.filter(status='approved').order_by('-created_at').first()
            if latest_application:
                return latest_application.household_income
        return None

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