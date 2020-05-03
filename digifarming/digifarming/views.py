from django.views import generic

from digifarming.models import User, Staff, Rating, \
    RequestType, Commodity, Supply, \
    Order, OrderItem, UserTrackingMovements, HarvestDispatch,FacilityType, Facility, \
    JobTitle, JobShift, ArrivalView, DepartureView, CancellationView, \
    TransportCategory, TransportType, TransportItems, Client, ClientType, CustomerTranportation
    # Hotel, ArrivalView, DepartureView, CancellationView, TodayBookingView, \
    # BookingSummaryView, InhouseGuestView, OverBookingView, RoomsOccupiedView, MostUsedFacilityView, \
    # LeastUsedFacilityView, AllOrdersListView, Laundry, LaundryType, LaundryItems, FacilityType, CleaningFacilityView, \
    # CleaningRoomView, User, Workers, Facilities
    # Alerts, AlertType
from operator import itemgetter
from django.db.utils import DatabaseError
from django import http
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages


from .forms import JobTitleForm, JobShiftForm, StaffForm, UserUpdateForm, UserForm, LoginForm



# Defining Generic views here.
def parse_update_params(request_params):
    result = dict()
    pk = request_params['pk']

    del request_params['pk']
    del request_params['csrfmiddlewaretoken']

    if 'name' in request_params and 'value' in request_params:
        result[request_params['name']] = request_params['value']
        del request_params['value']
        del request_params['name']

    result.update(**request_params)
    return pk, result


def _update_ajax(model_class, request):
    if request.method == 'POS,T' and request.is_ajax():
        pk, request_params = parse_update_params(request.POST.dict())
        model_class.objects.filter(pk=pk).update(**request_params)
        return model_class.objects.get(pk=pk)

# calling index page

# Listing all the arrivals in the system
class ArrivalListView(generic.ListView):
    template_name = ''
    context_object_name = 'arrival_list'
    model = ArrivalView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArrivalListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['booking_id'] = self.kwargs['booking_id']
        return context

    def get_queryset(self):
        # return ArrivalView.objects.filter(arrival_id=self.kwargs['arrival_id'])
        return ArrivalView.objects.order_by('start_date')


# Listing all the departures in the system
class DepartureListView(generic.ListView):
    template_name = ''
    context_object_name = 'departure_list'
    model = DepartureView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DepartureListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['booking_id'] = self.kwargs['booking_id']
        return context

    def get_queryset(self):
        return DepartureView.objects.order_by('end_date')


# Listing all the cancellations in the system
class CancellationListView(generic.ListView):
    template_name = ''
    context_object_name = 'guest_list'
    model = CancellationView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CancellationListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['booking_id'] = self.kwargs['booking_id']
        return context

    def get_queryset(self):
        return CancellationView.objects.order_by('booking_date')


# Getting today's summary - all totals
# class TodaySummaryListView(generic.ListView):
#     template_name = ''
#     context_object_name = 'today_summary_list'
#     model = TodayBookingView

#     def get_queryset(self):
#         return TodayBookingView.objects.all()


# creating a new check in to track users facility usage
def tracking_check_in_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                check_in = UserTrackingMovements()
                check_in.user_tracking = request_params.get('user_id')
                check_in.user_tracking_facility = request_params.get('facility_id')
                check_in.user_tracking_status = request_params.get('status')
                check_in.save()

                return http.HttpResponse(json.dumps(
                    {'id': check_in.id, 'checked_in_facility': check_in.facility_id,
                     'status': check_in.status}), status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. Tracking Check in not created")


# Getting tracking trends - most used facilities
# class MostUsedFacilityListView(generic.ListView):
#     template_name = ''
#     context_object_name = 'facilities_most_used_list'
#     model = MostUsedFacilityView

#     def get_queryset(self):
#         return MostUsedFacilityView.objects.all()


# Getting tracking trends - least used facilities
# class LeastUsedFacilityListView(generic.ListView):
#     template_name = ''
#     context_object_name = 'facilities_least_used_list'
#     model = LeastUsedFacilityView

#     def get_queryset(self):
#         return LeastUsedFacilityView.objects.all()

# TODO
# Creating a new order
def add_order_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                order = Order()
                order.order_status = request_params.get('order_status')
                order.order_client = request_params.get('order_client')
                order.paid = request_params.get('paid')
                order.created_by = request_params.get('created_by')
                order.save()
                return http.HttpResponse(
                    json.dumps({'id': order.id, 'order_status': order.order_status}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. booking not created")


# List all orders
# class AllOrdersListView(generic.ListView):
#     template_name = ''
#     context_object_name = 'all_orders_list'
#     model = AllOrdersListView

#     def get_queryset(self):
#         return AllOrdersListView.objects.all()


# Update order, cancell or process
def update_order_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            order = _update_ajax(Orders, request)
            return http.HttpResponse(
                json.dumps({'pk': order.id, 'status': order.order_status, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# Creating  new commodity
def add_commodity_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                commodity = Commodity()
                commodity.commodity_id = request_params.get('commodity_id')
                commodity.commodity_type = request_params.get('commodity_type')
                commodity.name = request_params.get('commodity_name')
                commodity.quantity = request_params.get('quantity')
                commodity.metric = request_params.get('metric')
                commodity.created_on = request_params.get('created_on')
                commodity.save()
                return http.HttpResponse(
                    json.dumps({'id': commodity.commodity_id, 'commodity_id': commodity.commodity_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all commodities
class AllCommodityListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_commodity_list'
    model = Commodity

    def get_queryset(self):
        return AllCommodityListView.objects.all()


# updating commodity
def update_commodity_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity = _update_ajax(Commodity, request)
            return http.HttpResponse(
                json.dumps({'pk': commodity.id, 'commodity_name': commodity.name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting commodity
def delete_commodity_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity = Commodity.objects.get(pk=request.POST.get('pk'))
            commodity_id = commodity.id
            commodity.delete()
            return http.HttpResponse(
                content='commodity <strong>{}</strong> has been successfully deleted'.format(commodity_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  new harvest
def add_harvest_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                harvest = HarvestDispatch()
                harvest.dispatch_commodity = request_params.get('dispatch_commodity')
                harvest.dispatch_created_by = request_params.get('user_id')
                harvest.dispatch_facility = request_params.get('dispatch_facility')
                harvest.dispatch_metric = request_params.get('dispatch_metric')
                harvest.dispatch_quantity = request_params.get('dispatch_quantity')
                harvest.dispatch_to_staff = request_params.get('dispatch_to_staff')
                harvest.save()
                return http.HttpResponse(
                    json.dumps({'id': harvest.id, 'dispatch_commodity': harvest.dispatch_commodity}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. harvest not created")


# List all harvest
class AllHarvestListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_harvest_list'
    model = HarvestDispatch

    def get_queryset(self):
        return AllHarvestListView.objects.all()


# updating harvest
def update_harvest_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            harvest = _update_ajax(HarvestDispatch, request)
            return http.HttpResponse(
                json.dumps({'pk': harvest.id, 'commodity_name': harvest.dispatch_commodity, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting harvest
def delete_commodity_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            harvest = HarvestDispatch.objects.get(pk=request.POST.get('pk'))
            harvest_id = harvest.id
            harvest.delete()
            return http.HttpResponse(
                content='harvest <strong>{}</strong> has been successfully deleted'.format(harvest_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# TODO DONE 
# Creating  a new supply
def add_supply_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                supply = Supply()
                supply.supply_quantity = request_params.get('supply_quantity')
                supply.supply_commodity = request_params.get('supply_commodity')
                supply.supply_metric = request_params.get('supply_metric')
                supply.supply_cost = request_params.get('supply_cost')
                supply.supply_client = request_params.get('supply_client')
                supply.supply_destination = request_params.get('supply_destination')
                supply.supply_latitude = request_params.get('supply_latitude')
                supply.supply_longitude = request_params.get('supply_longitude')
                supply.supply_created_by = request_params.get('supply_created_by')
                supply.created_on = request_params.get('created_on')
                supply.save()
                return http.HttpResponse(
                    json.dumps({'id': supply.id, 'supply_client': supply.supply_client}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all supplies
class AllsupplyListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_supplys_list'
    model = Supply

    def get_queryset(self):
        return AllsupplyListView.objects.all()


# updating supplies
def update_supply_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            supply = _update_ajax(Supply, request)
            return http.HttpResponse(
                json.dumps({'pk': supply.id, 'supply_commodity': supply.supply_commodity, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting supply
def delete_supply_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            supply = Supply.objects.get(pk=request.POST.get('pk'))
            supply_id = supply.id
            supply.delete()
            return http.HttpResponse(
                content='supply <strong>{}</strong> has been successfully deleted'.format(supply_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new staff
def add_worker_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:

                staff = Staff()

                staff.staff_id = request_params.get('worker_id')
                staff.staff_user = request_params.get('staff_user')
                staff.staff_job_title = request_params.get('staff_job_title')
                staff.staff_job_shift = request_params.get('staff_job_shift')
                staff.is_hr = request_params.get('is_hr')
                # staff.staff_created_by = request_params.get('staff_created_by')
                staff.save()
                
                return http.HttpResponse(
                    json.dumps({'id': staff.id, 'staff_id': staff.staff_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all staff
# class AllWorkersListView(generic.ListView):
#     template_name = ''
#     context_object_name = 'all_workers_list'
#     model = Staff

#     def get_queryset(self):
#         return AllWorkersListView.objects.all()


# # updating staff
# def update_worker_ajax(request, **kwargs):
#     if request.method == 'POST' and request.is_ajax():
#         try:
#             worker = _update_ajax(Staff, request)
#             return http.HttpResponse(
#                 json.dumps({'pk': staff.id, 'worker_staff': staff.staff_user }),
#                 status=201)
#         except DatabaseError as e:
#             return http.HttpResponse(status=400, content='An error occurred while processing your request')
#     return http.HttpResponse(status=400)


# # deleting a staff
# def delete_worker_ajax(request, **kwargs):
#     if request.method == 'POST' and request.is_ajax():
#         try:
#             worker = Staff.objects.get(pk=request.POST.get('pk'))
#             worker_id = worker.id
#             worker.delete()
#             return http.HttpResponse(
#                 content='staff <strong>{}</strong> has been successfully deleted'.format(worker_id), status=200)
#         except DatabaseError as e:
#             return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new facility
def add_facility_type_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                facility = FacilityType()

                facility.facility_type = request_params.get('facility_type')
                facility.created_on = request_params.get('created_on')
                facility.save()
                return http.HttpResponse(
                    json.dumps({'id': facility.id, 'facility_type': facility.facility_type}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all Facility types
class AllFacilityTypeListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_facility_type_list'
    model = FacilityType

    def get_queryset(self):
        return AllFacilityTypeListView.objects.all()


# updating facility type
def update_facility_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = _update_ajax(FacilityType, request)
            return http.HttpResponse(
                json.dumps({'pk': facility.id, 'facility_type': facility.facility_type, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting facility type
def delete_facility_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = FacilityType.objects.get(pk=request.POST.get('pk'))
            facility_type_id = facility.facility_type_id
            facility.delete()
            return http.HttpResponse(
                content='facility type <strong>{}</strong> has been successfully deleted'.format(facility_type_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new facility
def add_facility_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                facility = Facility

                facility.facility_number = request_params.get('facility_number')
                facility.facility_name = request_params.get('facility_name')
                facility.facility_type = request_params.get('facility_type')
                facility.facility_location = request_params.get('facility_location')
                facility.facility_capacity = request_params.get('facility_capacity')
                facility.created_on = request_params.get('created_on')
                facility.save()
                return http.HttpResponse(
                    json.dumps({'id': facility.id, 'facility_name': facility.facility_name}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all Facility
class AllFacilityListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_facility_list'
    model = Facility

    def get_queryset(self):
        return AllFacilityListView.objects.all()


# updating facility
def update_facility_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = _update_ajax(Facility, request)
            return http.HttpResponse(
                json.dumps({'pk': facility.id, 'facility_name': facility.facility_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a facility
def delete_facility_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = Facility.objects.get(pk=request.POST.get('pk'))
            facility_id = facility.facility_id
            facility.delete()
            return http.HttpResponse(
                content='facility <strong>{}</strong> has been successfully deleted'.format(facility_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new rating
def add_rating_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                rate = Ratings

                rate.user_id = request_params.get('user_id')
                rate.rating = request_params.get('rating')
                rate.comment = request_params.get('comment')
                rate.created_on = request_params.get('created_on')

                rate.save()
                return http.HttpResponse(
                    json.dumps({'id': rate.id, 'rating': rate.rating}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all ratings
class AllRatingsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_ratings_list'
    model = Facility

    def get_queryset(self):
        return AllRatingsListView.objects.all()


# updating a rating
def update_rating_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            rate = _update_ajax(Rating, request)
            return http.HttpResponse(
                json.dumps({'pk': rate.id }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a rating
def delete_rating_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            rate = Rating.objects.get(pk=request.POST.get('pk'))
            rating_id = rate.rating_id
            rate.delete()
            return http.HttpResponse(
                content='rating <strong>{}</strong> has been successfully deleted'.format(rating_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# TODO change the renders and the redirects

def user_register(request):
   if request.method == "POST":
       form = UserForm(request.POST)
       if form.is_valid():
           user = form.save(commit=False)
           user.created_on = timezone.now()
           user.save()
           messages.success(request, 'Registered successfully')
           return redirect('user_login')
   else:
       form = UserForm()
       return render(request, 'pages/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                try:
                    user = User.objects.get(email=email)
                    form.add_error('password', "invalid password")
                except User.DoesNotExist:
                    form.add_error('email', "invalid email address")

    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def add_job_title(request):
    if request.method == "POST":
        form = JobTitleForm(request.POST)
        if form.is_valid():
            job_title = form.save(commit=False)
            job_title.job_created_by = request.user
            job_title.save()
            messages.success(request, 'Job title was created successfully')
            return redirect('add_job_title')

    else:
        form = JobTitleForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_job_title.html', context)


@login_required
def all_job_title(request):
    job_titles = JobTitle.objects.select_related().filter(job_title_status=1)

    context = {
        'job_titles': job_titles
    }
    return render(request, 'pages/all_job_titles.html', context)


@login_required
def job_title_details(request, job_title_id):
    job_title = get_object_or_404(JobTitle, id=job_title_id)
    staff = Staff.objects.filter(staff_job_title=job_title, staff_user__status=1)

    context = {
        'job_title': job_title,
        'staff': staff
    }

    return render(request, 'pages/job_title_details.html', context)


@login_required
def update_job_title(request, job_title_id):
    job_title = JobTitle.objects.get(id=job_title_id)

    if request.method == "POST":
        form = JobTitleForm(request.POST, instance=job_title)

        if form.is_valid():
            job_title = form.save()
            messages.success(request, 'Job title was updated successfully')
            return redirect('update_job_title', job_title_id=job_title_id)

    else:
        form = JobTitleForm(instance=job_title)

    context = {
        'job_title': job_title,
        'form': form
    }

    return render(request, 'pages/update_job_title.html', context)


@login_required
def deactivate_job_title(request, job_title_id):
    job_title = JobTitle.objects.get(id=job_title_id)
    job_title.job_title_status = 0
    job_title.save(update_fields=['job_title_status'])
    messages.add_message(request, messages.SUCCESS, 'Job title removed successfully')
    return redirect('all_job_titles')


@login_required
def add_job_shift(request):
    if request.method == "POST":
        form = JobShiftForm(request.POST)
        if form.is_valid():
            job_shift = form.save(commit=False)
            job_shift.created_by = request.user
            job_shift.save()
            messages.success(request, 'Job shift was added successfully')
            return redirect('add_job_shift')

    else:
        form = JobShiftForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_job_shift.html', context)


@login_required
def all_job_shifts(request):
    job_shifts = JobShift.objects.filter(job_shift_status=1)

    context = {
        'job_shifts': job_shifts
    }

    return render(request, 'pages/all_job_shifts.html', context)


@login_required
def update_job_shift(request, job_shift_id):
    job_shift = JobShift.objects.get(id=job_shift_id)

    if request.method == "POST":
        form = JobShiftForm(request.POST, instance=job_shift)

        if form.is_valid():
            job_shift = form.save()
            messages.success(request, 'Job shift was updated successfully')
            return redirect('update_job_shift', job_shift_id=job_shift_id)

    else:
        form = JobShiftForm(instance=job_shift)

    context = {
        'job_shift': job_shift,
        'form': form
    }

    return render(request, 'pages/update_job_shift.html', context)


@login_required
def deactivate_job_shift(request, job_shift_id):
    job_shift = JobShift.objects.get(id=job_shift_id)
    job_shift.job_shift_status = 0
    job_shift.save(update_fields=['job_shift_status'])
    messages.add_message(request, messages.SUCCESS, 'Job shift removed successfully')
    return redirect('all_job_shifts')


@login_required
def add_staff(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            # Save general user details
            user = user_form.save(commit=False)
            user.is_staff = True
            user.save()

            # Save staff specific details
            staff = staff_form.save(commit=False)
            staff.staff_user = user
            staff.staff_created_by = request.user
            staff.save()

            # Success message
            messages.success(request, 'The staff has been successfully created')
            return redirect('add_staff')

    else:
        user_form = UserForm()
        staff_form = StaffForm()

    context = {
        'user_form': user_form,
        'staff_form': staff_form
    }

    return render(request, 'pages/add_staff.html', context)


@login_required
def current_staff(request):
    staff = Staff.objects.select_related().filter(staff_user__status=1)

    context = {
        'staff': staff
    }

    return render(request, 'pages/current_staff.html', context)


@login_required
def past_staff(request):
    staff = Staff.objects.select_related().filter(staff_user__status=0)

    context = {'staff': staff}

    return render(request, 'pages/past_staff.html', context)


@login_required
def update_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    user = User.objects.get(id=staff.staff_user.id)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        staff_form = StaffForm(request.POST, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            staff = staff_form.save()
            messages.success(request, 'Staff was updated successfully')

            return redirect('update_staff', staff_id=staff_id)

    else:
        user_form = UserUpdateForm(instance=user)
        staff_form = StaffForm(instance=staff)

    context = {
        'user_form': user_form,
        'staff_form': staff_form,
        'staff': staff
    }

    return render(request, 'pages/update_staff.html', context)


@login_required
def deactivate_staff(request, staff_id):
    # Update in user table
    user = User.objects.get(id=staff_id)
    user.status = 0
    user.save(update_fields=['status'])

    # Update in staff table
    staff = Staff.objects.get(staff_user=staff_id)
    staff.staff_end_date = timezone.now()
    staff.save(update_fields=['staff_end_date'])

    messages.add_message(request, messages.SUCCESS, 'Staff was removed successfully')
    return redirect('current_staff')