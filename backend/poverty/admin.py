from django.contrib import admin
from .models import PovertyApplication, AssistanceRecord

class AssistanceRecordInline(admin.TabularInline):
    model = AssistanceRecord
    extra = 0
    readonly_fields = ('assistance_date',)

@admin.register(PovertyApplication)
class PovertyApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'created_at', 'reviewed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'title', 'content')
    readonly_fields = ('created_at', 'reviewed_at')
    inlines = [AssistanceRecordInline]
    
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
    list_display = ('application', 'supporter', 'assistance_type', 'assistance_date')
    list_filter = ('assistance_type', 'assistance_date')
    search_fields = ('application__user__username', 'supporter__username', 'details')
    readonly_fields = ('assistance_date',)
    
    fieldsets = (
        ('援助信息', {
            'fields': ('application', 'supporter', 'assistance_type')
        }),
        ('详细信息', {
            'fields': ('details', 'assistance_date')
        }),
    )

    class Meta:
        verbose_name = '援助记录'
        verbose_name_plural = '援助记录管理'