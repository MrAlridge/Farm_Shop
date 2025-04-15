# poverty/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import User

class PovertyApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='poverty_applications'
    )
    title = models.CharField('申请标题', max_length=200)
    content = models.TextField('申请内容')
    status = models.CharField(
        '状态',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    reviewed_at = models.DateTimeField('审核时间', null=True, blank=True)
    review_comment = models.TextField('审核意见', null=True, blank=True)
    # 贫困户信息
    household_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    family_members = models.PositiveIntegerField(blank=True, null=True)
    reason_for_poverty = models.TextField(blank=True, null=True)  # 贫困原因
    # ... 其他字段，如家庭详细地址、联系方式、身份证照片等

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = '贫困户申请'
        verbose_name_plural = '贫困户申请'

class AssistanceRecord(models.Model):
    application = models.ForeignKey(PovertyApplication, on_delete=models.CASCADE,related_name='assistance_records')
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistance_records')
    assistance_type = models.CharField(max_length=50)  # 例如：物资援助、教育资助、技能培训
    assistance_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)  # 援助详情

    def __str__(self):
        return f"{self.supporter.username} - {self.assistance_type} - {self.assistance_date}"