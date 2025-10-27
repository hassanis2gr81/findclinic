from django.shortcuts import render, get_object_or_404
from .models import Doctor

def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'index.html', {'doctors': doctors})

def alldoctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'alldoctor.html', {'doctors': doctors})

"""doctor single page view start"""
def doctor_detail(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, 'profile1.html', {'doctor': doctor})
"""doctor single page view end"""
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def add_listing(request):
    return render(request, 'add_listing.html')