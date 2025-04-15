# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from users.serializers import UserSerializer
from products.models import Product # 导入 Product 模型

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True) #可以用于展示，但是创建时不用
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True) #用于创建
    subtotal = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    class Meta:
        model = OrderItem
        fields = ['id', 'product','product_id', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True)
    status = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_amount',)
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.calculate_total_amount()
        return order
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance = super().update(instance, validated_data)
        if items_data is not None:
            # 更新订单项。更复杂的逻辑是先删除旧的再创建新的
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
            instance.calculate_total_amount()

        return instance