from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, SocialSupport, PoorApplication

# 只取消注册 Group 模型
admin.site.unregister(Group)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('email', 'phone_number', 'avatar')}),
        ('用户类型', {'fields': ('user_type',)}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

@admin.register(SocialSupport)
class SocialSupportAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_person')
    search_fields = ('company_name', 'contact_person', 'user__username')
    list_filter = ('user__is_active',)

    class Meta:
        verbose_name = '社会帮扶单位'
        verbose_name_plural = '社会帮扶单位管理'

@admin.register(PoorApplication)
class PoorApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'reason')
    readonly_fields = ('created_at', 'reviewed_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'reason', 'status')
        }),
        ('审核信息', {
            'fields': ('review_comment', 'reviewed_at')
        }),
        ('证明材料', {
            'fields': ('supporting_documents',)
        }),
    )

    class Meta:
        verbose_name = '贫困户申请'
        verbose_name_plural = '贫困户申请管理'