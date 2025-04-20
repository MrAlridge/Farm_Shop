# orders/models.py
from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', '待发货'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders',limit_choices_to={'user_type': 'social'})
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # ... 其他字段（例如：收货地址、联系方式、支付方式、支付时间、物流信息等）

    # 收货地址相关信息
    shipping_address = models.CharField(max_length=255) # 假设只存一个字符串
    contact_phone = models.CharField(max_length=20)
    receiver_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username} - {self.get_status_display()}"

    def calculate_total_amount(self):
        """计算订单总金额"""
        total = 0
        for item in self.items.all():  # 访问 related_name='items' 的 OrderItem
            total += item.subtotal
        self.total_amount = total
        self.save()

class OrderItem(models.Model):
    SHIPPING_STATUS_CHOICES = (
        ('pending', '待发货'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,editable=False) #设置不允许编辑
    
    # 物流相关字段
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default='pending')
    shipping_company = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.order.id} - {self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        #更新订单的总价
        self.order.calculate_total_amount()
