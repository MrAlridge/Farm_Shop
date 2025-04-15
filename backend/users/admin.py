from django.contrib import admin
from .models import User, SocialSupport

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(SocialSupport)
class SocialSupport(admin.ModelAdmin):
    pass