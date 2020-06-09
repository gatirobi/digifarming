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

    # Facility
    path('facility/add/', views.add_facility_ajax, name='add-facility-ajax'),
    path('facility/type/', views.add_facility_type_ajax, name='add-facility-type-ajax'),

    # Client
    path('client/add/', views.add_client_ajax, name='add-client-ajax'),
    path('client/type/', views.add_client_type_ajax, name='add-client-type-ajax'),

    # Commodity
    path('commodity/add/', views.add_commodity_ajax, name='add-commodity-ajax'),
    path('commodity/category/', views.add_commodity_category_ajax, name='add-commodity-category-ajax'),
    path('commodity/metric/', views.add_commodity_metric_ajax, name='add-commodity-metric-ajax'),
    path('commodity/type/', views.add_commodity_type_ajax, name='add-commodity-type-ajax'),
  
    # Transport 
    path('transport/add/', views.add_transport_items_ajax, name='add-transport-items-ajax'),
    path('transport/category/', views.add_transport_category_ajax, name='add-transport-category-ajax'),
    path('transport/type/', views.add_transport_type_ajax, name='add-transport-type-ajax'),

    # Order 
    path('order/add/', views.add_order_ajax, name='add-order-ajax'),
    path('order/item/', views.add_order_item_ajax, name='add-order-item-ajax'),

    path('customer/transportation/', views.add_customer_transportation_ajax, name='add-customer-transportation-ajax'),
    path('harvest/', views.add_harvest_dispatch_ajax, name='add-harvest-dispatch-ajax'),
    path('supply/', views.add_supply_ajax, name='add-supply-ajax'),
    
    path('viz/', views.all_visualizations, name='view-visualizations'),  
    # Job titles
    path('job/titles/add/', views.add_job_title, name='add-job-title'),
    path('job/titles/all/', views.all_job_title, name='all-job-titles'),
    # path('job/titles/view/<str:job_title_id>', views.job_title_details, name='job_title_details'),
    path('job/titles/update/<str:job_title_id>', views.update_job_title, name='update-job-title'),
    path('job/titles/remove/<str:job_title_id>', views.deactivate_job_title, name='deactivate-job-title'),

    # Job shifts
    path('job/shifts/add/', views.add_job_shift, name='add-job-shift'),
    path('job/shifts/all/', views.all_job_shifts, name='all-job-shifts'),
    path('job/shifts/update/<str:job_shift_id>', views.update_job_shift, name='update-job-shift'),
    path('job/shifts/deactivate/<str:job_shift_id>', views.deactivate_job_shift, name='deactivate-job-shift'),

    # Staff
    path('staff/add/', views.add_staff, name='add-staff'),
    path('staff/current/', views.current_staff, name='current-staff'),
    path('staff/past/', views.past_staff, name='past-staff'),
    path('staff/update/<str:staff_id>', views.update_staff, name='update-staff'),
    path('staff/deactivate/<str:staff_id>', views.deactivate_staff, name='deactivate-staff'),

]
