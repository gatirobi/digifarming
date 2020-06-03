from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from hashid_field import HashidAutoField

from digifarming.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = (('Female', 'Female'), ('Male', 'Male'))

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(null=False, unique=True)
    phone = models.CharField(max_length=50, null=False)
    created_on = models.DateTimeField(null=False, default=timezone.now)
    is_staff = models.BooleanField(null=False,default=False)
    is_client = models.BooleanField(null=False, default=False)
    is_superuser = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)
    status = models.IntegerField(default=1, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def publish_user(self):
        self.created_on = timezone.now
        self.save()

    def __str__(self):
        return self.get_full_name()


class JobTitle(models.Model):
    id = HashidAutoField(primary_key=True)
    job_title = models.CharField(max_length=100, null=False)
    job_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    job_created_on = models.DateTimeField(default=timezone.now)
    job_title_status = models.IntegerField(default=1)

    def __str__(self):
        return self.job_title


class JobShift(models.Model):
    id = HashidAutoField(primary_key=True)
    job_shift = models.CharField(max_length=100, null=False)
    shift_start_time = models.TimeField(null=False)
    shift_end_time = models.TimeField(null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now, null=False)
    job_shift_status = models.IntegerField(default=1)

    def __str__(self):
        return self.job_shift


class Staff(models.Model):
    id = HashidAutoField(primary_key=True)
    staff_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_user')
    staff_id = models.CharField(null=False, max_length=100)
    staff_job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    staff_job_shift = models.ForeignKey(JobShift, on_delete=models.CASCADE)
    is_hr = models.BooleanField(null=False, default=False)
    staff_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_created_by')
    staff_end_date = models.DateTimeField(blank=True, null=True)


# class Client(models.Model):
#     customer_user = models.OneToOneField(User, on_delete=models.CASCADE)
#     customer_name = models.CharField(null=False, max_length=100)


class FacilityType(models.Model):
    id = HashidAutoField(primary_key=True)
    facility_type_name = models.CharField(max_length=100, null=False)
    facility_type_status = models.IntegerField(null=False,default=1)
    facility_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    facility_type_created_on = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return self.facility_type_name


class Facility(models.Model):
    id = HashidAutoField(primary_key=True)
    facility_type = models.ForeignKey(FacilityType, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=50, null=False)
    facility_location = models.CharField(max_length=50, null=False)
    facility_capacity = models.IntegerField(null=False)
    status = models.IntegerField(null=False, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

# Cleaning
class Cleaning(models.Model):
    cleaning_staff = models.ForeignKey(User, on_delete=models.CASCADE)
    cleaning_facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    cleaning_time = models.DateTimeField(default=timezone.now)


class Rating(models.Model):
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=False)
    rating_comment = models.TextField(blank=True)
    rating_created_on = models.DateTimeField(default=timezone.now)

class Chat(models.Model):
    chat_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    chat_recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    chat_message = models.CharField(max_length=700, null=True)
    chat_type = models.CharField(max_length=100, null=False)
    chat_time = models.DateTimeField(null=False, default=timezone.now)

class RequestType(models.Model):
    request_type_name = models.CharField(max_length=50, null=False)
    request_type_created_on = models.DateTimeField(default=timezone.now)
    request_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.request_type_name


class Request(models.Model):
    request_user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_request_type = models.ForeignKey(RequestType, models.CASCADE)
    request_created_on = models.DateTimeField(default=timezone.now)


class AlertType(models.Model):
    alert_type_name = models.CharField(null=False, max_length=100)
    alert_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type_created_on = models.DateTimeField(null=False, default=timezone.now)

    def __str__(self):
        return self.alert_type_name


class Alert(models.Model):
    alert_title = models.ForeignKey(AlertType, on_delete=models.CASCADE)
    alert_message = models.TextField(null=False)
    alert_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_created_on = models.DateTimeField(default=timezone.now)


class CommodityCategory(models.Model):
    commodity_category_name = models.CharField(max_length=100, null=False)
    commodity_category_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity_category_created_on = models.DateTimeField(null=False, default=timezone.now)
    commodity_category_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.commodity_category_name


class CommodityType(models.Model):
    commodity_category = models.ForeignKey(CommodityCategory, on_delete=models.CASCADE)
    commodity_type_name = models.CharField(max_length=100, null=False)
    commodity_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity_type_created_on = models.DateTimeField(null=False, default=timezone.now)
    commodity_type_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.commodity_type_name


class CommodityMetric(models.Model):
    commodity_metric_name = models.CharField(max_length=100, null=False)
    commodity_metric_created_on = models.DateTimeField(null=False, default=timezone.now)
    commodity_metric_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity_metric_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.commodity_metric_name


class Commodity(models.Model):
    commodity_category = models.ForeignKey(CommodityCategory, on_delete=models.CASCADE)
    commodity_type = models.ForeignKey(CommodityType, on_delete=models.CASCADE)
    commodity_name = models.CharField(max_length=100, null=False)
    commodity_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    commodity_created_on = models.DateTimeField(null=False, default=timezone.now)
    commodity_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.commodity_name

class TransportCategory(models.Model):
    transport_category_name = models.CharField(max_length=100, null=False)
    transport_category_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_category_created_on = models.DateTimeField(null=False, default=timezone.now)
    transport_category_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.transport_category_name


class TransportType(models.Model):
    transport_category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE)
    transport_type_name = models.CharField(max_length=100, null=False)
    transport_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_type_created_on = models.DateTimeField(null=False, default=timezone.now)
    transport_type_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.transport_type_name

class TransportItems(models.Model):
    transport_category = models.ForeignKey(TransportCategory, on_delete=models.CASCADE)
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    transport_name = models.CharField(max_length=100, null=False)
    transport_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_created_on = models.DateTimeField(null=False, default=timezone.now)
    transport_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.transport_name

class ClientType(models.Model):
    client_type_name = models.CharField(max_length=100, null=False)
    client_type_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    client_type_created_on = models.DateTimeField(null=False, default=timezone.now)
    client_type_status = models.IntegerField(null=False, default=1)

    def __str__(self):
        return self.client_type_name


class Client(models.Model):
    client_full_name = models.CharField(max_length=100, null=False)
    client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    client_phone = models.CharField(max_length=100, null=False)
    client_email = models.EmailField(max_length=100, null=False, unique=True)
    client_created_on = models.DateTimeField(default=timezone.now)
    client_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    client_status = models.IntegerField(null=False, default=1)

# Supplying stuff to the client
class Supply(models.Model):
    supply_commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    supply_quantity = models.IntegerField(null=False)
    supply_metric = models.ForeignKey(CommodityMetric, on_delete=models.CASCADE)
    supply_cost = models.IntegerField(null=False)
    supply_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    supply_destination = models.CharField(max_length=100, null=False)
    supply_latitude = models.CharField(max_length=100, null=False)
    supply_longitude = models.CharField(max_length=100, null=False)
    supply_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    supply_created_on = models.DateTimeField(null=False, default=timezone.now)

# DispatchStock
class HarvestDispatch(models.Model):
    dispatch_commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    dispatch_quantity = models.IntegerField(null=False)
    dispatch_metric = models.ForeignKey(CommodityMetric, on_delete=models.CASCADE)
    dispatch_to_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    dispatch_facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    dispatch_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dispatcher')
    dispatch_created_on = models.DateTimeField(default=timezone.now)

class CustomerTransportation(models.Model):
    customer_commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    customer_transport_item = models.ForeignKey(TransportItems, on_delete=models.CASCADE)
    customer_quantity = models.IntegerField(null=False)
    customer_metric = models.ForeignKey(CommodityMetric, on_delete=models.CASCADE)
    customer_cost = models.IntegerField(null=False)
    customer_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    customer_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_created_on = models.DateTimeField(null=False, default=timezone.now)

class Order(models.Model):
    order_created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    order_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_name = models.CharField(max_length=100, null=False)
    order_status = models.IntegerField(null=False, default=1)
    order_paid = models.BooleanField(null=False, default=True)
    order_created_on = models.DateTimeField(default=timezone.now)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    order_type = models.ForeignKey(CommodityType, on_delete=models.CASCADE)
    order_item_quantity = models.IntegerField(null=False, default=1)
    order_item_cost = models.IntegerField(null=False)



class UserTrackingMovements(models.Model):
    user_tracking = models.ForeignKey(User, on_delete=models.CASCADE)
    user_tracking_facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    user_tracking_status = models.CharField(max_length=100, null=False)
    user_tracking_created_on = models.DateTimeField(default=timezone.now)

# Views definitions
class ArrivalView(models.Model):
    class Meta:
        managed = False
        db_table = 'ArrivalsView'


class DepartureView(models.Model):
    class Meta:
        managed = False
        db_table = 'DeparturesView'

class CancellationView(models.Model):
    class Meta:
        managed = False
        db_table = 'CancellationView'
