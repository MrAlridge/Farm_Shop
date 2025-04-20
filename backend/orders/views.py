# orders/views.py
from rest_framework import viewsets, status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list':
              permission_classes = [IsAuthenticated]
        else:
              permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_queryset(self):
        """
        管理员可以查看所有订单,用户只能查看自己的订单
        """
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':  # 假设只有待支付状态的订单可以取消
                order.status = 'cancelled'
                order.save()
                serializer = self.get_serializer(order)
                return Response(serializer.data)
        else:
            return Response({'message': 'Order cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def pending_shipping(self, request):
        """获取贫困户待发货的订单项"""
        # 检查用户类型
        if request.user.user_type != 'poor':
            return Response({'error': '非贫困户用户'}, status=status.HTTP_403_FORBIDDEN)

        # 获取该贫困户的待发货订单项
        order_items = OrderItem.objects.filter(
            product__added_by=request.user,  # 使用 added_by 字段
            order__status='pending'  # 只获取已支付的订单
        ).select_related('order', 'product')

        # 按订单分组
        orders = {}
        for item in order_items:
            order_id = item.order.id
            if order_id not in orders:
                orders[order_id] = {
                    'id': order_id,
                    'order_date': item.order.order_date,
                    'total_amount': item.order.total_amount,
                    'items': []
                }
            orders[order_id]['items'].append({
                'id': item.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'shipping_status': item.shipping_status
            })

        return Response(list(orders.values()))

    @action(detail=True, methods=['post'])
    def ship_item(self, request, pk=None):
        """发货单个订单项"""
        order = self.get_object()
        item_id = request.data.get('item_id')
        tracking_number = request.data.get('tracking_number')
        shipping_company = request.data.get('shipping_company')

        if not all([item_id, tracking_number, shipping_company]):
            return Response({'error': '缺少必要参数'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = OrderItem.objects.get(id=item_id, order=order)
            # 检查当前用户是否有权限发货该商品
            if request.user.user_type != 'poor' or item.product.added_by != request.user:
                return Response({'error': '无权操作此订单项'}, status=status.HTTP_403_FORBIDDEN)

            item.shipping_status = 'shipped'
            item.tracking_number = tracking_number
            item.shipping_company = shipping_company
            item.save()

            # 检查是否所有订单项都已发货
            all_shipped = not OrderItem.objects.filter(
                order=order,
                shipping_status='pending'
            ).exists()

            if all_shipped:
                order.status = 'shipped'
                order.save()

            return Response({'message': '发货成功'})
        except OrderItem.DoesNotExist:
            return Response({'error': '订单项不存在'}, status=status.HTTP_404_NOT_FOUND)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'poor':
            return OrderItem.objects.filter(product__added_by=self.request.user)
        return OrderItem.objects.none()

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """发货单个订单项"""
        order_item = self.get_object()
        
        # 检查当前用户是否有权限发货该商品
        if request.user.user_type != 'poor' or order_item.product.added_by != request.user:
            return Response({'error': '无权操作此订单项'}, status=status.HTTP_403_FORBIDDEN)

        # 更新订单项的发货状态
        order_item.shipping_status = 'shipped'
        order_item.save()

        # 检查是否所有订单项都已发货
        all_shipped = not OrderItem.objects.filter(
            order=order_item.order,
            shipping_status='pending'
        ).exists()

        if all_shipped:
            order_item.order.status = 'shipped'
            order_item.order.save()

        return Response({'message': '发货成功'})