from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'sales', 'added_by', 'created_at')
    list_filter = ('category', 'added_by__user_type', 'created_at')
    search_fields = ('name', 'description', 'added_by__username')
    readonly_fields = ('created_at', 'updated_at', 'sales')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'category', 'price', 'stock')
        }),
        ('图片信息', {
            'fields': ('image',)
        }),
        ('销售信息', {
            'fields': ('sales',)
        }),
        ('发布信息', {
            'fields': ('added_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建商品
            obj.added_by = request.user
        super().save_model(request, obj, form, change)