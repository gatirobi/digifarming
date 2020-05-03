"""digifarming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.urls import path, re_path, include
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
     path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    # Job titles
    path('job/titles/add/', views.add_job_title, name='add_job_title'),
    path('job/titles/all/', views.all_job_title, name='all_job_titles'),
    path('job/titles/view/<str:job_title_id>', views.job_title_details, name='job_title_details'),
    path('job/titles/update/<str:job_title_id>', views.update_job_title, name='update_job_title'),
    path('job/titles/remove/<str:job_title_id>', views.deactivate_job_title, name='deactivate_job_title'),

    # Job shifts
    path('job/shifts/add/', views.add_job_shift, name='add_job_shift'),
    path('job/shifts/all/', views.all_job_shifts, name='all_job_shifts'),
    path('job/shifts/update/<str:job_shift_id>', views.update_job_shift, name='update_job_shift'),
    path('job/shifts/deactivate/<str:job_shift_id>', views.deactivate_job_shift, name='deactivate_job_shift'),

    # Staff
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/current/', views.current_staff, name='current_staff'),
    path('staff/past/', views.past_staff, name='past_staff'),
    path('staff/update/<str:staff_id>', views.update_staff, name='update_staff'),
    path('staff/deactivate/<str:staff_id>', views.deactivate_staff, name='deactivate_staff'),

]
