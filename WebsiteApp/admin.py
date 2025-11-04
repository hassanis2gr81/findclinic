from django.contrib import admin
from django import forms
from .models import City, Clinic, Category, Address, Service, Doctor, DoctorClinic,Blog

# --------------------
# City Admin
# --------------------
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# --------------------
# Clinic Admin
# --------------------
@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)


# --------------------
# Category Admin
# --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)


# --------------------
# Address Admin
# --------------------
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'nearabout', 'city')
    search_fields = ('name', 'city__name')
    list_filter = ('city',)


# --------------------
# Service Admin
# --------------------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('name',)


# --------------------
# Inline for DoctorClinic (must be defined BEFORE DoctorAdmin)
# --------------------
class DoctorClinicInline(admin.TabularInline):
    model = DoctorClinic
    extra = 1
    autocomplete_fields = ['clinic']
    fields = ('clinic', 'days', 'start_time', 'end_time')
    show_change_link = True  # allows editing existing records
    verbose_name = "Clinic Schedule"
    verbose_name_plural = "Clinic Schedules"

    def save_new_instance(self, form, commit=True):
        # ensure the instance is saved correctly to the doctor
        instance = form.save(commit=False)
        if commit:
            instance.save()
        return instance


# --------------------
# Doctor Model Form (to include Admin JS/CSS)
# --------------------
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

    class Media:
        css = {
            'all': (
                # Select2 CSS
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                # Flatpickr CSS (time picker)
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            )
        }
        js = (
            # jQuery (Django admin already has it but safe to include CDN fallback)
            'https://code.jquery.com/jquery-3.6.0.min.js',
            # Select2
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            # Flatpickr
            'https://cdn.jsdelivr.net/npm/flatpickr',
            # Your custom admin JS (must be at static/admin/js/doctor_city_clinic.js)
            'admin/js/doctor_city_clinic.js',
        )


# --------------------
# Doctor Admin
# --------------------
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorForm
    list_display = ('name', 'specialization', 'city', 'experience_years', 'rating')
    search_fields = ('name', 'specialization', 'city__name')
    list_filter = ('city', 'categories', 'rating')
    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = ('categories', 'addresses', 'services')

    inlines = [DoctorClinicInline]

    def save_formset(self, request, form, formset, change):
        """
        Ensure DoctorClinic relationships persist properly.
        """
        instances = formset.save(commit=False)
        for instance in instances:
            instance.doctor = form.instance  # reattach doctor explicitly
            instance.save()
        formset.save_m2m()  # Save M2M fields


# --------------------
# Blog admin
# --------------------

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'author')
    list_filter = ('is_published', 'created_at')