from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SocialSupport, PoorApplication

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'phone_number', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('用户类型', {'fields': ('user_type',)}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'email', 'phone_number'),
        }),
    )

@admin.register(SocialSupport)
class SocialSupportAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'contact_person')
    search_fields = ('company_name', 'contact_person', 'user__username')
    list_filter = ('user__is_active',)

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