# products/serializers.py
from rest_framework import serializers
from .models import Product, Category
from users.serializers import UserSerializer
class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #用于展示分类下的产品
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    added_by = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many = False)
    image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = '__all__'
    def create(self, validated_data):
       # 自动设置申请用户为当前请求用户
        validated_data['added_by'] = self.context['request'].user
        return super().create(validated_data)