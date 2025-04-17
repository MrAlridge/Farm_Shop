from django.contrib import admin
from .models import PovertyApplication, AssistanceRecord

@admin.register(PovertyApplication)
class PovertyApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'title', 'content')
    readonly_fields = ('created_at', 'reviewed_at')
    
    fieldsets = (
        ('申请信息', {
            'fields': ('user', 'title', 'content', 'status')
        }),
        ('家庭信息', {
            'fields': ('household_income', 'family_members', 'reason_for_poverty')
        }),
        ('审核信息', {
            'fields': ('review_comment', 'reviewed_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            from django.utils import timezone
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

    class Meta:
        verbose_name = '扶贫申请'
        verbose_name_plural = '扶贫申请管理'

@admin.register(AssistanceRecord)
class AssistanceRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'supporter', 'status', 'start_date', 'end_date', 'deadline')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'supporter__username', 'contact_person')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'image', 'description', 'content')
        }),
        ('时间安排', {
            'fields': ('start_date', 'end_date', 'deadline')
        }),
        ('联系方式', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('其他信息', {
            'fields': ('supporter', 'status', 'created_at', 'updated_at')
        }),
    )

    class Meta:
        verbose_name = '帮扶项目'
        verbose_name_plural = '帮扶项目管理'