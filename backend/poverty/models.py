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
    name = models.CharField('项目名称', max_length=200)
    image = models.ImageField('项目图片', upload_to='assistance_images/', null=True, blank=True)
    description = models.TextField('项目简介', default='')
    content = models.TextField('项目内容', default='')
    start_date = models.DateField('开始日期')
    end_date = models.DateField('结束日期')
    deadline = models.DateField('报名截止日期')
    contact_person = models.CharField('联系人', max_length=100, default='')
    contact_phone = models.CharField('联系电话', max_length=20, default='')
    contact_email = models.EmailField('联系邮箱', default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    supporter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='assistance_records',
        limit_choices_to={'user_type': 'social'}
    )
    status = models.CharField(
        '状态',
        max_length=20,
        choices=(
            ('draft', '草稿'),
            ('published', '已发布'),
            ('closed', '已结束'),
        ),
        default='draft'
    )

    def __str__(self):
        return f"{self.name} - {self.supporter.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = '帮扶项目'
        verbose_name_plural = '帮扶项目'