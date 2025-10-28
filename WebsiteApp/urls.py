from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('add-listing/', views.add_listing, name='add_listing'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('alldoctor/', views.alldoctor, name='alldoctor'),
    path('listofdoctor/', views.listofdoctor, name='listofdoctor'),
    
    
]
