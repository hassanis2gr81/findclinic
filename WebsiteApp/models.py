from django.db import models
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# =====================
# ✅ City Model
# =====================
class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='city_images/', blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================
# ✅ Category Model
# =====================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', default='category/default.png', blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    meta_description = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================
# ✅ Clinic Model
# =====================
class Clinic(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='clinics', null=True, blank=True)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    detail = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='clinic_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.city.name if self.city else 'No City'})"


# =====================
# ✅ Address Model
# =====================
class Address(models.Model):
    name = models.CharField(max_length=255)
    nearabout = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f"{self.name}, {self.city.name}"


# =====================
# ✅ Service Model
# =====================
class Service(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================
# ✅ Doctor Model
# =====================
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, default='Unknown')
    email = models.EmailField(default='unknown@example.com')
    phone = models.CharField(max_length=15, default='0000000000')
    image = models.ImageField(upload_to='doctor/', default='doctor/default.jpg')
    experience_years = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    clinics = models.ManyToManyField(Clinic, through='DoctorClinic', related_name='doctor_clinics')
    categories = models.ManyToManyField(Category, blank=True, related_name='doctors')
    addresses = models.ManyToManyField(Address, blank=True, related_name='doctors')
    services = models.ManyToManyField(Service, blank=True, related_name='doctors')

    slug = models.SlugField(unique=True, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)
    reviews = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================
# ✅ DoctorClinic Model
# =====================
class DoctorClinic(models.Model):
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE)
    clinic = models.ForeignKey("Clinic", on_delete=models.CASCADE)

    DAYS_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    days = MultiSelectField(choices=DAYS_CHOICES, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.name} at {self.clinic.name} ({self.days or 'No days'})"

# =====================
# ✅ For Blog post model
# ===================== 

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=100, default='Admin')
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    short_description = models.CharField(max_length=300, blank=True, null=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

