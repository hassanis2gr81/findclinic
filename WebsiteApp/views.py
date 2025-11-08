from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor, City, Category, Service, Clinic, Testimonial, Blog, BlogCategory, PatientProfile
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# ---------------------- PUBLIC VIEWS ----------------------

def home(request):
    doctors = Doctor.objects.all()
    cities = City.objects.all()
    categories = Category.objects.all()
    testimonials = Testimonial.objects.all()[:10]
    blogs_home = Blog.objects.all().order_by('-created_at')[:6]
    return render(request, 'index.html', {
        'doctors': doctors,
        'cities': cities,
        'categories': categories,
        'testimonials': testimonials,
        'blogs': blogs_home,
    })


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})


def clinic(request):
    doctors = Doctor.objects.all()
    return render(request, 'clinic.html', {'doctors': doctors})


def blog(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-id')
    recent_posts = Blog.objects.filter(is_published=True).order_by('-created_at')[:5]
    blog_categories = BlogCategory.objects.all()

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'blog_categories': blog_categories
    })


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    recent_posts = Blog.objects.exclude(id=blog.id).order_by('-created_at')[:6]
    blog_categories = BlogCategory.objects.all()
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'recent_posts': recent_posts,
        'blog_categories': blog_categories
    })


def blog_category(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    blogs = Blog.objects.filter(category=category, is_published=True)
    recent_posts = Blog.objects.order_by('-created_at')[:5]
    blog_categories = BlogCategory.objects.all()

    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'blog_categories': blog_categories,
        'category': category
    })


def doctor_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    doctors = Doctor.objects.filter(categories=category)
    return render(request, 'alldoctor.html', {'category': category, 'doctors': doctors})


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

    return render(request, 'search-list-view-1.html', {
        'doctors': doctors,
        'cities': City.objects.all(),
        'categories': Category.objects.all(),
        'services': Service.objects.all(),
        'selected_city': city_id,
        'selected_category': category_id,
        'selected_service': service_id,
        'search_query': search_query,
    })


def doctor_detail(request, slug):
    doctor = get_object_or_404(Doctor, slug=slug)
    return render(request, 'profile1.html', {'doctor': doctor})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def add_listing(request):
    return render(request, 'add_listing.html')


def load_clinics(request):
    city_id = request.GET.get('city') or request.GET.get('city_id')
    if not city_id:
        return JsonResponse([], safe=False)
    clinics = Clinic.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(clinics), safe=False)


def doctors_by_city_and_category(request, city_slug, category_slug):
    city = get_object_or_404(City, name__iexact=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    doctors = Doctor.objects.filter(city=city, categories=category).distinct()

    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search-list-view-1.html', {
        'city': city,
        'category': category,
        'page_obj': page_obj
    })


# ---------------------- DOCTOR AUTH ----------------------

def doctor_login(request):
    if request.user.is_authenticated and hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user and hasattr(user, 'doctor'):
            auth.login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a doctor account!')
    return render(request, 'doctor_login.html')


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

        user = User.objects.create_user(username=username, email=email, password=password)
        Doctor.objects.create(user=user, name=username, email=email)
        login(request, user)
        return redirect('doctor_dashboard')

    return render(request, 'doctor_signup.html')


@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED: Redirect to home instead of patient_dashboard
    doctor = request.user.doctor
    return render(request, 'dashboard/dashboard_doctor.html', {'doctor': doctor})


@login_required(login_url='doctor_login')
def doctor_profile_edit(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED

    doctor = request.user.doctor
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


@login_required(login_url='doctor_login')
def doctor_clinic_add(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED

    cities = City.objects.all()
    clinics = Clinic.objects.all()
    doctor = request.user.doctor

    if request.method == 'POST':
        clinic = Clinic.objects.get(id=request.POST.get('clinic'))
        city = City.objects.get(id=request.POST.get('city'))
        doctor.city = city
        doctor.clinics.add(clinic)
        doctor.save()
        messages.success(request, 'Clinic added successfully!')
        return redirect('doctor_dashboard')

    return render(request, 'doctor_clinic_add.html', {'cities': cities, 'clinics': clinics})


def doctor_logout(request):
    logout(request)
    return redirect('doctor_login')

#doctor_schedule k liye

@login_required(login_url='doctor_login')
def doctor_schedule(request):
    # Only allow doctors to access
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/doctor_schedule.html')

#doctor_reports k liye
@login_required(login_url='doctor_login')
def doctor_reports(request):
    # Only allow doctors to access
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/doctor_reports.html')

#doctor_patients k liye
@login_required(login_url='doctor_login')
def doctor_patients(request):
    # Only allow doctors to access
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/doctor_patients.html')




# ---------------------- PATIENT AUTH ----------------------

def patient_login(request):
    if request.user.is_authenticated and hasattr(request.user, 'patient_profile'):
        return redirect('patient_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user and hasattr(user, 'patient_profile'):
            login(request, user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a patient account!')
    return render(request, 'patient_login.html')


def patient_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('patient_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('patient_signup')

        user = User.objects.create_user(username=email, email=email, password=password)
        PatientProfile.objects.create(user=user, name=name)
        login(request, user)
        return redirect('patient_dashboard')

    return render(request, 'patient_signup.html')


@login_required(login_url='patient_login')
def patient_dashboard(request):
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Patient account required to access this page.')
        return redirect('home')  # ✅ FIXED: Redirect to home instead of doctor_dashboard
    profile = request.user.patient_profile
    return render(request, 'dashboard/dashboard_patient.html', {'profile': profile})


@login_required(login_url='patient_login')
def patient_appointments(request):
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Patient account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/patient_appointments.html')


@login_required(login_url='patient_login')
def patient_records(request):
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Patient account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/patient_records.html')


@login_required(login_url='patient_login')
def patient_reports(request):
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Patient account required to access this page.')
        return redirect('home')  # ✅ FIXED
    return render(request, 'dashboard/patient_reports.html')


def patient_logout(request):
    logout(request)
    return redirect('patient_login')

@login_required
def login_redirect(request):
    if hasattr(request.user, 'doctor'):
        return redirect('doctor_dashboard')
    elif hasattr(request.user, 'patient_profile'):
        return redirect('patient_dashboard')
    else:
        return redirect('home')
    

@login_required(login_url='doctor_login')
def doctor_add_info(request):
    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Doctor account required to access this page.')
        return redirect('home')
    
    doctor = request.user.doctor
    
    if request.method == 'POST':
        try:
            # Update basic information
            doctor.name = request.POST.get('name', doctor.name)
            doctor.specialization = request.POST.get('specialization', doctor.specialization)
            doctor.qualification = request.POST.get('qualification', doctor.qualification)
            doctor.phone = request.POST.get('phone', doctor.phone)
            doctor.email = request.POST.get('email', doctor.email)
            doctor.experience_years = request.POST.get('experience_years', doctor.experience_years)
            doctor.description = request.POST.get('description', doctor.description)
            
            # Update image if provided
            if 'image' in request.FILES:
                doctor.image = request.FILES['image']
            
            doctor.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctor_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'dashboard/doctor_add_info.html', {'doctor': doctor})