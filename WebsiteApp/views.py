from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor, City, Category, Service, Clinic
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

def home(request):
    doctors = Doctor.objects.all()
    cities = City.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'doctors': doctors, 'cities': cities, 'categories': categories})

# show all catgories
def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})

def clinic(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic.html', {'doctors': doctors})

def blog(request):
    doctors = Doctor.objects.all()
    return render(request, 'blog.html', {'doctors': doctors})

def alldoctor(request):
    doctors = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search-list-view-1.html', {'page_obj': page_obj})

def listofdoctor(request):
    city_id = request.GET.get('city')
    category_id = request.GET.get('category')
    service_id = request.GET.get('service')
    search_query = request.GET.get('q')

    doctors = Doctor.objects.all()

    if city_id:
        doctors = doctors.filter(city_id=city_id)
    if category_id:
        doctors = doctors.filter(categories__id=category_id)
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
    return render(request, 'search-list-view-1.html', context)

def doctor_detail(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, 'profile1.html', {'doctor': doctor})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    return render(request, 'login.html')

def add_listing(request):
    return render(request, 'add_listing.html')

def load_clinics(request):
    city_id = request.GET.get('city') or request.GET.get('city_id')
    if not city_id:
        return JsonResponse([], safe=False)
    clinics = Clinic.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(clinics), safe=False)

# ✅ NEW VIEW: City + Category page (like findclinic/lahore/dermatologist)
def doctors_by_city_and_category(request, city_slug, category_slug):
    # Get the city and category objects
    city = get_object_or_404(City, name__iexact=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    
    # ✅ Filter doctors by the selected city and category
    doctors = Doctor.objects.filter(
        city=city,
        categories=category
    ).distinct()

    # ✅ Pagination
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # ✅ Render template
    return render(request, 'search-list-view-1.html', {
        'city': city,
        'category': category,
        'page_obj': page_obj,
    })

"""doctor signup code"""

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'login.html')


# SIGNUP
def doctor_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('doctor_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('doctor_signup')

        # create user with no admin permissions
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=False,   # ❌ not admin/staff
            is_superuser=False  # ❌ not superuser
        )

        # create related doctor profile
        Doctor.objects.create(name=username, email=email)

        # ✅ auto login new doctor
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

        messages.success(request, 'Account created & logged in successfully!')
        return redirect('doctor_dashboard')

    return render(request, 'login.html')

# DASHBOARD
@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    doctor = Doctor.objects.filter(email=request.user.email).first()
    return render(request, 'doctor_dashboard.html', {'doctor': doctor})


# LOGOUT
def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')


# PROFILE EDIT
@login_required(login_url='doctor_login')
def doctor_profile_edit(request):
    doctor = Doctor.objects.filter(email=request.user.email).first()
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')
        doctor.phone = request.POST.get('phone')
        doctor.experience_years = request.POST.get('experience_years')
        doctor.description = request.POST.get('description')
        doctor.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('doctor_dashboard')
    return render(request, 'doctor_profile_edit.html', {'doctor': doctor})


# CLINIC ADD
@login_required(login_url='doctor_login')
def doctor_clinic_add(request):
    cities = City.objects.all()
    clinics = Clinic.objects.all()
    doctor = Doctor.objects.filter(email=request.user.email).first()

    if request.method == 'POST':
        clinic_id = request.POST.get('clinic')
        city_id = request.POST.get('city')
        clinic = Clinic.objects.get(id=clinic_id)
        city = City.objects.get(id=city_id)
        doctor.city = city
        doctor.clinics.add(clinic)
        doctor.save()
        messages.success(request, 'Clinic added successfully!')
        return redirect('doctor_dashboard')

    return render(request, 'doctor_clinic_add.html', {'cities': cities, 'clinics': clinics})