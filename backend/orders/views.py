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
    # def perform_create(self, serializer): #已经在序列化器中完成
    #     serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
      # 订单条目必须依附订单，所以只允许管理员查看和操作
      if self.request.user.is_staff:
          return OrderItem.objects.all()
      return OrderItem.objects.none()