from django.db import models
from django.utils.text import slugify

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, default='Unknown')
    email = models.EmailField(default='unknown@example.com')
    phone = models.CharField(max_length=15, default='0000000000')
    address = models.CharField(max_length=255, default='Unknown')
    image = models.ImageField(upload_to='doctor/', default='doctor/default.jpg')
    experience_years = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    # ⭐ New fields for home page
    rating = models.PositiveSmallIntegerField(default=0)  # 0-5 stars
    reviews = models.PositiveIntegerField(default=0)      # total number of reviews

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
