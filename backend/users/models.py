# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', '管理员'),
        ('poor', '贫困户'),
        ('social', '社会帮扶人员'),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='social'
    )
    phone_number = models.CharField(max_length=15, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_groups",  # 添加 related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",  # 添加 related_name
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class SocialSupport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'social'}, related_name='social_profile')
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    # ... 其他字段

class PoorApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='poor_applications')
    reason = models.TextField(verbose_name='申请原因')
    supporting_documents = models.FileField(upload_to='poor_applications/', null=True, blank=True, verbose_name='证明材料')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='申请时间')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    review_comment = models.TextField(null=True, blank=True, verbose_name='审核意见')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '贫困户申请'
        verbose_name_plural = '贫困户申请'