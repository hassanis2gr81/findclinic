from django.contrib import admin
from django import forms
from .models import City, Clinic, Category, Address, Service, Doctor, DoctorClinic, Blog, Testimonial, BlogCategory,PatientProfile

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
    show_change_link = True
    verbose_name = "Clinic Schedule"
    verbose_name_plural = "Clinic Schedules"

    def save_new_instance(self, form, commit=True):
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
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            'https://cdn.jsdelivr.net/npm/flatpickr',
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
        instances = formset.save(commit=False)
        for instance in instances:
            instance.doctor = form.instance
            instance.save()
        formset.save_m2m()


# --------------------
# Blog Admin
# --------------------
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'author')
    list_filter = ('is_published', 'created_at')


# --------------------
# Blog Category Admin
# --------------------
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('created_at',)


# --------------------
# Testimonial Admin
# --------------------
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'created_at')
    search_fields = ('name', 'position', 'message')


# --------------------
# Pateint Admin
# --------------------
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'created_at')
    search_fields = ('user__email','name','phone')