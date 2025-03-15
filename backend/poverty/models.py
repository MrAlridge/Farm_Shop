# poverty/models.py
from django.db import models
from users.models import User

class PovertyApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '未通过'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poor_profile',limit_choices_to={'user_type': 'poor'})
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # 贫困户信息
    household_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    family_members = models.PositiveIntegerField(blank=True, null=True)
    reason_for_poverty = models.TextField(blank=True, null=True)  # 贫困原因
    # ... 其他字段，如家庭详细地址、联系方式、身份证照片等

    def __str__(self):
      return f"{self.user.username} - {self.get_status_display()}"

class AssistanceRecord(models.Model):
    application = models.ForeignKey(PovertyApplication, on_delete=models.CASCADE,related_name='assistance_records')
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistance_records')
    assistance_type = models.CharField(max_length=50)  # 例如：物资援助、教育资助、技能培训
    assistance_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)  # 援助详情

    def __str__(self):
        return f"{self.supporter.username} - {self.assistance_type} - {self.assistance_date}"