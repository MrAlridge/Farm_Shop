from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total_amount', 'receiver_name', 'contact_phone')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'receiver_name', 'contact_phone', 'shipping_address')
    readonly_fields = ('order_date', 'total_amount')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('订单信息', {
            'fields': ('user', 'status', 'total_amount', 'order_date')
        }),
        ('收货信息', {
            'fields': ('receiver_name', 'contact_phone', 'shipping_address')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            # 如果订单状态改变，可以在这里添加相应的处理逻辑
            pass
        super().save_model(request, obj, form, change)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单管理'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项管理'