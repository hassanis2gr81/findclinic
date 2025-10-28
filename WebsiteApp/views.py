from django.shortcuts import render, get_object_or_404
from .models import Doctor, City, Category, Service
from django.db.models import Q

def home(request):
    doctors = Doctor.objects.all()
    return render(request, 'index.html', {'doctors': doctors})

def alldoctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'alldoctor.html', {'doctors': doctors})

"""all doctor list here"""
def listofdoctor(request):
    city_id = request.GET.get('city')
    category_id = request.GET.get('category')
    service_id = request.GET.get('service')
    search_query = request.GET.get('q')  # for text search (optional)

    doctors = Doctor.objects.all()

    # Apply filters
    if city_id:
        doctors = doctors.filter(city_id=city_id)
    if category_id:
        doctors = doctors.filter(category_id=category_id)
    if service_id:
        doctors = doctors.filter(services__id=service_id)
    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) |
            Q(specialization__icontains=search_query) |
            Q(city__name__icontains=search_query)
        ).distinct()

    context = {
        'doctors': doctors,
        'cities': City.objects.all(),
        'categories': Category.objects.all(),
        'services': Service.objects.all(),
        'selected_city': city_id,
        'selected_category': category_id,
        'selected_service': service_id,
        'search_query': search_query,
    }
    return render(request, 'listofdoctor.html', context)

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