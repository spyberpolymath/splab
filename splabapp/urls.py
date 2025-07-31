from django.urls import path
from . import views
from .views import home, combined_create, successful_fixed_list, successful_fixed_detail, successful_fixed_create

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Bug URLs
    path('bugs/', views.bug_list, name='bug_list'),
    path('bugs/<int:pk>/', views.bug_detail, name='bug_detail'),
    path('contact/', views.contact, name='contact'),
    path('docs/', views.docs, name='docs'),
    path('usage/', views.usage, name='usage'),
    path('setup/', views.setup, name='setup'),
    # Create URL
    path('create/', combined_create, name='combined_create'),
    # Successful Fixed URLs
    path('successful_fixed/', successful_fixed_list, name='successful_fixed_list'),
    path('successful_fixed/create/', successful_fixed_create, name='successful_fixed_create'),
    path('successful_fixed/<int:pk>/', successful_fixed_detail, name='successful_fixed_detail'),
    path('researcher_list/', views.researcher_list, name='researcher_list'),
    path('researcher_detail/<str:category>/<int:obj_id>/', views.researcher_detail, name='researcher_detail'),
] 