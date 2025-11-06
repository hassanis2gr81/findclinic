from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # ---------------- Doctor Auth ----------------
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('doctor_logout/', views.doctor_logout, name='doctor_logout'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('doctor/clinic/add/', views.doctor_clinic_add, name='doctor_clinic_add'),
    path('doctor/reports/', views.doctor_reports, name='doctor_reports'),
    path('doctor/schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),


    # ---------------- Patient Auth ----------------
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),
    path('patient_logout/', views.patient_logout, name='patient_logout'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('patient/records/', views.patient_records, name='patient_records'),
    path('patient/reports/', views.patient_reports, name='patient_reports'),

    # Website content
    path('add-listing/', views.add_listing, name='add_listing'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('alldoctor/', views.alldoctor, name='alldoctor'),
    path('listofdoctor/', views.listofdoctor, name='listofdoctor'),
    path('ajax/load-clinics/', views.load_clinics, name='ajax_load_clinics'),
    path('clinics/', views.clinic, name='clinic'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/category/<slug:slug>/', views.blog_category, name='blog_category'),

    # All categories
    path('all-categories/', views.all_categories, name='all_categories'),

    # Dynamic filter
    path('<slug:city_slug>/<slug:category_slug>/', views.doctors_by_city_and_category, name='doctors_by_city_and_category'),
    path('doctors/category/<slug:slug>/', views.doctor_by_category, name='doctor_by_category'),
]
