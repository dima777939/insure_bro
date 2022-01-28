from django.contrib import admin
from .models import InsuranceCompany


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'description']


