from django.views import generic

from digifarming.models import User, Staff, Rating, \
    RequestType, Commodity, Supply, \
    Order, OrderItem, UserTrackingMovements, HarvestDispatch,FacilityType, Facility, \
    JobTitle, JobShift, ArrivalView, DepartureView, CancellationView, \
    TransportCategory, TransportType, TransportItems, Client, ClientType, CustomerTransportation, \
    CommodityCategory, CommodityType, CommodityMetric, Commodity, HarvestDispatch    

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

from .forms import JobTitleForm, JobShiftForm, StaffForm, UserUpdateForm, UserForm, LoginForm, \
    FacilityForm, FacilityTypeForm, ClientTypeForm, ClientForm, CommodityCategoryForm, CommodityTypeForm, \
    CommodityMetricForm, CommodityForm, TransportCategoryForm, TransportTypeForm, TransportItemsForm, \
    CustomerTransportationForm, HarvestDispatchForm, OrderItemForm, OrderForm, SupplyForm



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
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_created_by_id = request.user.id
            order.save()
            messages.success(request, 'Order was added successfully')
            return redirect('add-order-item-ajax')

    else:
        form = OrderForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_order.html', context)


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
            order = _update_ajax(Order, request)
            return http.HttpResponse(
                json.dumps({'pk': order.id, 'status': order.order_status, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)

# deleting a order
def delete_order_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            order = Order.objects.get(pk=request.POST.get('pk'))
            order_id = order.id
            order.delete()
            return http.HttpResponse(
                content='order <strong>{}</strong> has been successfully deleted'.format(order_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new order item
def add_order_item_ajax(request, **kwargs):
    if request.method == "POST":
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request, 'Order Item was added successfully')
            return redirect('add-order-item-ajax')

    else:
        form = OrderItemForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_order_item.html', context)

# List all order items
class AllOrderItemListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_order_list'
    model = OrderItem

    def get_queryset(self):
        return AllOrderItemListView.objects.all()


# updating order item
def update_order_item_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            order = _update_ajax(OrderItem, request)
            return http.HttpResponse(
                json.dumps({'pk': order.id, 'order_name': order.order_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a order item
def delete_order_item_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            order = OrderItem.objects.get(pk=request.POST.get('pk'))
            order_id = order.id
            order.delete()
            return http.HttpResponse(
                content='order <strong>{}</strong> has been successfully deleted'.format(order_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new supply item
def add_supply_ajax(request, **kwargs):
    if request.method == "POST":
        form = SupplyForm(request.POST)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.supply_created_by_id = request.user.id
            supply.save()
            messages.success(request, 'Supply was added successfully')
            return redirect('add-supply-ajax')

    else:
        form = SupplyForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_supply.html', context)

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
                # staff.staff_created_by_id = request_params.get('staff_created_by')
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

# Creating  a new harvest dispatch
def add_harvest_dispatch_ajax(request, **kwargs):
    if request.method == "POST":
        form = HarvestDispatchForm(request.POST)
        if form.is_valid():
            harvest_dispatch = form.save(commit=False)
            harvest_dispatch.dispatch_to_staff_id = request.user.id
            harvest_dispatch.dispatch_created_by_id = request.user.id
            harvest_dispatch.save()
            messages.success(request, 'Transport dispatch was added successfully')
            return redirect('add-harvest-dispatch-ajax')

    else:
        form = HarvestDispatchForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_harvest_dispatch.html', context)

# List all harvest dispatch
class AllHarvestDispatchListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_harvest_dispatch_list'
    model = HarvestDispatch

    def get_queryset(self):
        return AllHarvestDispatchListView.objects.all()


# updating harvest dispatch
def update_harvest_dispatch_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            harvest_dispatch = _update_ajax(HarvestDispatch, request)
            return http.HttpResponse(
                json.dumps({'pk': harvest_dispatch.id, 'dispatch_commodity': harvest_dispatch.dispatch_commodity, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a harvest dispatch
def delete_harvest_dispatch_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            harvest_dispatch = HarvestDispatch.objects.get(pk=request.POST.get('pk'))
            harvest_dispatch_id = harvest_dispatch.id
            harvest_dispatch.delete()
            return http.HttpResponse(
                content='harvest_dispatch <strong>{}</strong> has been successfully deleted'.format(harvest_dispatch_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new customer transportation
def add_customer_transportation_ajax(request, **kwargs):
    if request.method == "POST":
        form = CustomerTransportationForm(request.POST)
        if form.is_valid():
            customer_transportation = form.save(commit=False)
            customer_transportation.customer_created_by_id = request.user.id
            customer_transportation.save()
            messages.success(request, 'Transport transportation was added successfully')
            return redirect('add-customer-transportation-ajax')

    else:
        form = CustomerTransportationForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_customer_transportation.html', context)

# List all customer transportation
class AllCustomerTransportationListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_customer_transportation_list'
    model = CustomerTransportation

    def get_queryset(self):
        return AllCustomerTransportationListView.objects.all()


# updating customer transportation
def update_customer_transportation_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            customer_transportation = _update_ajax(CustomerTransportation, request)
            return http.HttpResponse(
                json.dumps({'pk': customer_transportation.id, 'customer_transportation_name': customer_transportation.customer_transportation_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a customer transportation
def delete_customer_transportation_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            customer_transportation = CustomerTransportation.objects.get(pk=request.POST.get('pk'))
            customer_transportation_id = customer_transportation.id
            customer_transportation.delete()
            return http.HttpResponse(
                content='customer_transportation <strong>{}</strong> has been successfully deleted'.format(customer_transportation_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new transport items
def add_transport_items_ajax(request, **kwargs):
    if request.method == "POST":
        form = TransportItemsForm(request.POST)
        if form.is_valid():
            transport_items = form.save(commit=False)
            transport_items.transport_created_by_id = request.user.id
            transport_items.save()
            messages.success(request, 'Transport item was added successfully')
            return redirect('add-transport-items-ajax')

    else:
        form = TransportItemsForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_transport_items.html', context)

# List all transport items
class AllTransportItemsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_transport_items_list'
    model = TransportItems

    def get_queryset(self):
        return AllTransportItemsListView.objects.all()


# updating transport items
def update_transport_items_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_items = _update_ajax(TransportItems, request)
            return http.HttpResponse(
                json.dumps({'pk': transport_items.id, 'transport_items_name': transport_items.transport_items_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a transport items
def delete_transport_items_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_items = TransportItems.objects.get(pk=request.POST.get('pk'))
            transport_items_id = transport_items.transport_items_id
            transport_items.delete()
            return http.HttpResponse(
                content='transport_items <strong>{}</strong> has been successfully deleted'.format(transport_items_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new transport type
def add_transport_type_ajax(request, **kwargs):
    if request.method == "POST":
        form = TransportTypeForm(request.POST)
        if form.is_valid():
            transport_type = form.save(commit=False)
            transport_type.transport_type_created_by_id = request.user.id
            transport_type.save()
            messages.success(request, 'Transport type was added successfully')
            return redirect('add-transport-type-ajax')

    else:
        form = TransportTypeForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_transport_type.html', context)

# List all transport type
class AllTransportTypeListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_transport_type_list'
    model = TransportType

    def get_queryset(self):
        return AllTransportTypeListView.objects.all()


# updating transport type
def update_transport_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_type = _update_ajax(TransportType, request)
            return http.HttpResponse(
                json.dumps({'pk': transport_type.id, 'transport_type_name': transport_type.transport_type_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a transport type
def delete_transport_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_type = TransportType.objects.get(pk=request.POST.get('pk'))
            transport_type_id = transport_type.transport_type_id
            transport_type.delete()
            return http.HttpResponse(
                content='transport_type <strong>{}</strong> has been successfully deleted'.format(transport_type_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new transport category
def add_transport_category_ajax(request, **kwargs):
    if request.method == "POST":
        form = TransportCategoryForm(request.POST)
        if form.is_valid():
            transport_category = form.save(commit=False)
            transport_category.transport_category_created_by_id = request.user.id
            transport_category.save()
            messages.success(request, 'Transport category was added successfully')
            return redirect('add-transport-category-ajax')

    else:
        form = TransportCategoryForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_transport_category.html', context)

# List all transport category
class AllTransportCategoryListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_transport_category_list'
    model = TransportCategory

    def get_queryset(self):
        return AllTransportCategoryListView.objects.all()


# updating transport category
def update_transport_category_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_category = _update_ajax(TransportCategory, request)
            return http.HttpResponse(
                json.dumps({'pk': transport_category.id, 'transport_category_name': transport_category.transport_category_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a transport category
def delete_transport_category_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            transport_category = TransportCategory.objects.get(pk=request.POST.get('pk'))
            transport_category_id = transport_category.transport_category_id
            transport_category.delete()
            return http.HttpResponse(
                content='transport_category <strong>{}</strong> has been successfully deleted'.format(transport_category_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new commodity
def add_commodity_ajax(request, **kwargs):
    if request.method == "POST":
        form = CommodityForm(request.POST)
        if form.is_valid():
            commodity = form.save(commit=False)
            commodity.commodity_created_by_id = request.user.id
            commodity.save()
            messages.success(request, 'Commodity was added successfully')
            return redirect('add-commodity-ajax')

    else:
        form = CommodityForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_commodity.html', context)

# List all commodity
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
                json.dumps({'pk': commodity.id, 'commodity_name': commodity.commodity_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a commodity
def delete_commodity_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity = Commodity.objects.get(pk=request.POST.get('pk'))
            commodity_id = commodity.commodity_id
            commodity.delete()
            return http.HttpResponse(
                content='commodity <strong>{}</strong> has been successfully deleted'.format(commodity_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new commodity metric
def add_commodity_metric_ajax(request, **kwargs):
    if request.method == "POST":
        form = CommodityMetricForm(request.POST)
        if form.is_valid():
            commodity_metric = form.save(commit=False)
            commodity_metric.commodity_metric_created_by_id = request.user.id
            commodity_metric.save()
            messages.success(request, 'Commodity metric was added successfully')
            return redirect('add-commodity-metric-ajax')

    else:
        form = CommodityMetricForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_commodity_metric.html', context)

# List all commodity metric
class AllCommodityMetricListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_commodity_metric_list'
    model = CommodityMetric

    def get_queryset(self):
        return AllCommodityMetricListView.objects.all()


# updating commodity metric
def update_commodity_metric_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_metric = _update_ajax(CommodityMetric, request)
            return http.HttpResponse(
                json.dumps({'pk': commodity_metric.id, 'commodity_metric_name': commodity_metric.commodity_metric_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a commodity metric
def delete_commodity_metric_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_metric = CommodityMetric.objects.get(pk=request.POST.get('pk'))
            commodity_metric_id = commodity_metric.commodity_metric_id
            commodity_metric.delete()
            return http.HttpResponse(
                content='commodity_metric <strong>{}</strong> has been successfully deleted'.format(commodity_metric_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new commodity type
def add_commodity_type_ajax(request, **kwargs):
    if request.method == "POST":
        form = CommodityTypeForm(request.POST)
        if form.is_valid():
            commodity_type = form.save(commit=False)
            commodity_type.commodity_type_created_by_id = request.user.id
            commodity_type.save()
            messages.success(request, 'Commodity type was added successfully')
            return redirect('add-commodity-type-ajax')

    else:
        form = CommodityTypeForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_commodity_type.html', context)

# List all commodity type
class AllCommodityTypeListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_commodity_type_list'
    model = CommodityType

    def get_queryset(self):
        return AllCommodityTypeListView.objects.all()


# updating commodity type
def update_commodity_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_type = _update_ajax(CommodityType, request)
            return http.HttpResponse(
                json.dumps({'pk': commodity_type.id, 'commodity_type_name': commodity_type.commodity_type_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a commodity type
def delete_commodity_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_type = CommodityType.objects.get(pk=request.POST.get('pk'))
            commodity_type_id = commodity_type.commodity_type_id
            commodity_type.delete()
            return http.HttpResponse(
                content='commodity_type <strong>{}</strong> has been successfully deleted'.format(commodity_type_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')

# Creating  a new commodity category
def add_commodity_category_ajax(request, **kwargs):
    if request.method == "POST":
        form = CommodityCategoryForm(request.POST)
        if form.is_valid():
            commodity_category = form.save(commit=False)
            commodity_category.commodity_category_created_by_id = request.user.id
            commodity_category.save()
            messages.success(request, 'Commodity Category was added successfully')
            return redirect('add-commodity-category-ajax')

    else:
        form = CommodityCategoryForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_commodity_category.html', context)

# List all commodity category
class AllCommodityCategoryListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_commodity_category_list'
    model = CommodityCategory

    def get_queryset(self):
        return AllCommodityCategoryListView.objects.all()


# updating commodity category
def update_commodity_category_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_category = _update_ajax(CommodityCategory, request)
            return http.HttpResponse(
                json.dumps({'pk': commodity_category.id, 'commodity_category_name': commodity_category.commodity_category_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a commodity category
def delete_commodity_category_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity_category = CommodityCategory.objects.get(pk=request.POST.get('pk'))
            commodity_category_id = commodity_category.commodity_category_id
            commodity_category.delete()
            return http.HttpResponse(
                content='commodity_category <strong>{}</strong> has been successfully deleted'.format(commodity_category_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new client
def add_client_ajax(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.client_created_by_id = request.user.id
                client.save()
                messages.success(request, 'client was added successfully')
                return redirect('add-client-type-ajax')
                # return reverse('digifarming:add-client-ajax')
            except (ValueError, KeyError):
                messages.add_message(request, messages.ERROR, 'Invalid values encountered, Server Error')

        # if form.is_valid():
        #     client = form.save(commit=False)
        #     client.client_created_by_id = request.user.id
        #     client.save()
        #     messages.success(request, 'Client was added successfully')
        #     return redirect('add_client_ajax')

    else:
        form = ClientForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_client.html', context)

# List all Client
class AllClientListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_client_list'
    model = Client

    def get_queryset(self):
        return AllClientListView.objects.all()


# updating client
def update_client_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            client = _update_ajax(Client, request)
            return http.HttpResponse(
                json.dumps({'pk': client.id, 'client_name': client.client_full_name, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a client
def delete_client_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            client = Client.objects.get(pk=request.POST.get('pk'))
            client_id = client.client_id
            client.delete()
            return http.HttpResponse(
                content='client <strong>{}</strong> has been successfully deleted'.format(client_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new client type
def add_client_type_ajax(request):
    if request.method == "POST":
        form = ClientTypeForm(request.POST)
        if form.is_valid():
            try:
                client_type = form.save(commit=False)
                client_type.client_type_created_by_id = request.user.id
                client_type.save()
                messages.success(request, 'client type was added successfully')
                return redirect('add-client-type-ajax')
                # return reverse('digifarming:add-client-ajax')
            except (ValueError, KeyError):
                messages.add_message(request, messages.ERROR, 'Invalid values encountered, Server Error')

    else:
        form = ClientTypeForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_client_type.html', context)


# List all client types
class AllClientTypeListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_client_type_list'
    model = ClientType

    def get_queryset(self):
        return AllClientTypeListView.objects.all()


# updating client type
def update_client_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            client_type = _update_ajax(ClientType, request)
            return http.HttpResponse(
                json.dumps({'pk': client_type.id, 'client_type': client_type.client_type, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting client type
def delete_client_type_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            client = ClientType.objects.get(pk=request.POST.get('pk'))
            client_type_id = client.client_type_id
            client.delete()
            return http.HttpResponse(
                content='client type <strong>{}</strong> has been successfully deleted'.format(client_type_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')



# Creating  a new facility type
def add_facility_type_ajax(request, **kwargs):
    if request.method == "POST":
        form = FacilityTypeForm(request.POST)
        if form.is_valid():
            facility_type = form.save(commit=False)
            facility_type.facility_type_created_by_id = request.user.id
            facility_type.save()
            messages.success(request, 'Facility type was added successfully')
            return redirect('add-facility-type-ajax')

    else:
        form = FacilityTypeForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_facility_type.html', context)


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
@login_required
def add_facility_ajax(request, **kwargs):
    if request.method == "POST":
        form = FacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.created_by_id = request.user.id
            facility.save()
            messages.success(request, 'Facility was added successfully')
            return redirect('add-facility-ajax')

    else:
        form = FacilityForm()

    context = {
        'form': form
    }

    return render(request, 'pages/add_facility.html', context)

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

# TODO
# Creating  a new rating
def add_rating_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                rate = Rating

                rate.user_id = request_params.get('user_id')
                rate.rating = request_params.get('rating')
                rate.comment = request_params.get('comment')

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
           user.save()
           messages.success(request, 'Registered successfully')
           return redirect('user_login')
       else:
           return render(request, 'pages/register.html', {'form': form}) 
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
                return redirect('add-facility-ajax')
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


# @login_required
def add_job_title(request):
    if request.method == "POST":
        form = JobTitleForm(request.POST)
        if form.is_valid():
            job_title = form.save(commit=False)
            job_title.job_created_by_id = request.user.id
            job_title.save()
            messages.success(request, 'Job title was created successfully')
            return redirect('add-job-title')

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


# def job_title_details(request, job_title_id):
#     job_title = get_object_or_404(JobTitle, id=job_title_id)
#     staff = Staff.objects.filter(staff_job_title=job_title, staff_user__status=1)

#     context = {
#         'job_title': job_title,
#         'staff': staff
#     }

#     return render(request, 'pages/job_title_details.html', context)


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
            job_shift.created_by_id = request.user.id
            job_shift.save()
            messages.success(request, 'Job shift was added successfully')
            return redirect('add-job-shift')

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


# @login_required
def add_staff(request):
    if request.method == "POST":
        # user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)

        if staff_form.is_valid():
            # Save general user details
            # user = user_form.save(commit=False)
            # user.is_staff = True
            # user.save()
            

            # Save staff specific details
            staff = staff_form.save(commit=False)
            # staff.staff_user_id = user.id
            staff.staff_created_by_id = request.user.id
            staff.save()

            # Success message
            messages.success(request, 'The staff has been successfully created')
            return redirect('add-staff')

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

def all_visualizations(request):
    context = {'name': 'Visualization'}
    return render(request, 'pages/visualization.html', context)