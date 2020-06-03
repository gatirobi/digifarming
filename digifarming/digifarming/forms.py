from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import JobTitle, JobShift, User, Staff, Facility, FacilityType, ClientType, Client, \
    CommodityCategory, CommodityType, CommodityMetric, Commodity, TransportCategory, TransportType, TransportItems, \
    CustomerTransportation, HarvestDispatch, Order, OrderItem,  Supply    


class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ('job_title',)


class JobShiftForm(forms.ModelForm):
    class Meta:
        model = JobShift
        fields = ('job_shift', 'shift_start_time', 'shift_end_time')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')


class StaffForm(forms.ModelForm):
  class Meta:
    model = Staff
    fields = ('staff_id', 'staff_job_title', 'staff_job_shift', 'is_hr')


# class (UserCreationForm):
#    class Meta:
#        model = User
#        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('facility_name', 'facility_type', 'facility_location', 'facility_capacity')    


class FacilityTypeForm(forms.ModelForm):
    class Meta:
        model = FacilityType
        fields = ('facility_type_name',)

class ClientTypeForm(forms.ModelForm):
    class Meta:
        model = ClientType
        fields = ('client_type_name',)

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('client_full_name','client_type','client_phone','client_email')

class CommodityCategoryForm(forms.ModelForm):
    class Meta:
        model = CommodityCategory
        fields = ('commodity_category_name',)

class CommodityTypeForm(forms.ModelForm):
    class Meta:
        model = CommodityType
        fields = ('commodity_category','commodity_type_name')

class CommodityMetricForm(forms.ModelForm):
    class Meta:
        model = CommodityMetric
        fields = ('commodity_metric_name',)

class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ('commodity_category','commodity_type','commodity_name')

class TransportCategoryForm(forms.ModelForm):
    class Meta:
        model = TransportCategory
        fields = ('transport_category_name',)

class TransportTypeForm(forms.ModelForm):
    class Meta:
        model = TransportType
        fields = ('transport_category','transport_type_name')

class TransportItemsForm(forms.ModelForm):
    class Meta:
        model = TransportItems
        fields = ('transport_category','transport_type','transport_name')

class CustomerTransportationForm(forms.ModelForm):
    class Meta:
        model = CustomerTransportation
        fields = ('customer_commodity','customer_transport_item','customer_quantity','customer_metric', 'customer_cost', 'customer_client')

class HarvestDispatchForm(forms.ModelForm):
    class Meta:
        model = HarvestDispatch
        fields = ('dispatch_commodity','dispatch_quantity','dispatch_metric','dispatch_to_staff','dispatch_facility')

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('order','order_item','order_type','order_item_quantity', 'order_item_cost')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_client','order_name')

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ('supply_commodity','supply_quantity','supply_metric','supply_cost','supply_client','supply_destination','supply_latitude','supply_longitude')
