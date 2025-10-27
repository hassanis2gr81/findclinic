from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience_years', 'email')
    search_fields = ('name', 'specialization', 'email')
    prepopulated_fields = {'slug': ('name',)}  # slug auto fill in admin

