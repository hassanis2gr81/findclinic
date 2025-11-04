from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Auth routes
    path('login/', views.doctor_login, name='doctor_login'),
    path('signup/', views.doctor_signup, name='doctor_signup'),
    path('logout/', views.doctor_logout, name='doctor_logout'),

    # Doctor dashboard & profile
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('clinic/add/', views.doctor_clinic_add, name='doctor_clinic_add'),

    # Website content
    path('add-listing/', views.add_listing, name='add_listing'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('alldoctor/', views.alldoctor, name='alldoctor'),
    path('listofdoctor/', views.listofdoctor, name='listofdoctor'),
    path('ajax/load-clinics/', views.load_clinics, name='ajax_load_clinics'),
    path('clinics/', views.clinic, name='clinic'),
    path('blog/', views.blog, name='blog'),

    #show all categoies
    path('all-categories/', views.all_categories, name='all_categories'),


    # Dynamic filter
    path('<slug:city_slug>/<slug:category_slug>/', views.doctors_by_city_and_category, name='doctors_by_city_and_category'),
]