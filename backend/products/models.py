# products/models.py
from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True) #需要安装Pillow库
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products',limit_choices_to={'user_type': 'poor'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
      # ... 其他字段（例如：生产日期、保质期、产地等）
    def __str__(self):
        return self.name