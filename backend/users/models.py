# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('poor', '贫困户'),
        ('social', '社会力量'),
        ('admin', '管理员'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='poor')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

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

class SocialSupport(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'social'}, related_name='social_profile')
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    # ... 其他字段