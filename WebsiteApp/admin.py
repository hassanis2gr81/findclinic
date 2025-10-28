from django.contrib import admin
from .models import City, Clinic, Category, Address, Service, Doctor


# 🏙 City Admin
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# 🏥 Clinic Admin
@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)


# 🩺 Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)


# 📍 Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'nearabout', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)


# 🧾 Service Admin
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)


# 👩‍⚕️ Doctor Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience_years', 'rating', 'reviews')
    search_fields = ('name', 'specialization', 'city__name')
    list_filter = ('city', 'categories', 'clinics', 'services', 'rating')
    prepopulated_fields = {'slug': ('name',)}

    # Many-to-Many relationships (nice horizontal selector)
    filter_horizontal = ('categories', 'clinics', 'addresses', 'services')
