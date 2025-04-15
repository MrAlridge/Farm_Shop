from django.contrib import admin
from .models import PovertyApplication, AssistanceRecord

@admin.register(PovertyApplication)
class PovertyApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(AssistanceRecord)
class AssistanceRecordAdmin(admin.ModelAdmin):
    pass