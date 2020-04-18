from django.views import generic

from digifarming.models import User, Rooms, Workers, Cleaning, Facilities, Vehicles, Ratings, Parking, Events, Chats, \
    Booking, Requests, UserType, RequestType, Alerts, AlertType, Food, Drink, Commodity, Suppliers, Supplies, Menu, \
    Orders, OrderItem, UserTrackingMovements,
    # Hotel, ArrivalView, DepartureView, CancellationView, TodayBookingView, \
    # BookingSummaryView, InhouseGuestView, OverBookingView, RoomsOccupiedView, MostUsedFacilityView, \
    # LeastUsedFacilityView, AllOrdersListView, Laundry, LaundryType, LaundryItems, FacilityType, CleaningFacilityView, \
    # CleaningRoomView, User
from operator import itemgetter
from django.db.utils import DatabaseError
from django import http
import json


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
    if request.method == 'POST' and request.is_ajax():
        pk, request_params = parse_update_params(request.POST.dict())
        model_class.objects.filter(pk=pk).update(**request_params)
        return model_class.objects.get(pk=pk)


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


# Listing all the guests
class GuestListView(generic.ListView):
    template_name = ''
    context_object_name = 'guest_list'
    model = DepartureView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GuestListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['guest_id'] = self.kwargs['guest_id']
        return context

    def get_queryset(self):
        return InhouseGuestView.objects.order_by('guest_id')


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


# Listing all the over-bookings in the system
class OverbookingListView(generic.ListView):
    template_name = ''
    context_object_name = 'guest_list'
    model = OverBookingView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OverbookingListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['booking_id'] = self.kwargs['booking_id']
        return context

    def get_queryset(self):
        return OverBookingView.objects.order_by('booking_date')


# Listing all the rooms occupied
class RoomsOccupiedListView(generic.ListView):
    template_name = ''
    context_object_name = 'guest_list'
    model = RoomsOccupiedView
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RoomsOccupiedListView, self).get_context_data(**kwargs)
        request_params = self.request.GET.copy()
        if 'page' in request_params:
            del request_params['page']

        request_params = filter(itemgetter(1), request_params.items())

        if request_params:
            context['request_params'] = request_params

        context['booking_id'] = self.kwargs['booking_id']
        return context

    def get_queryset(self):
        return RoomsOccupiedView.objects.order_by('booking_date')


# Getting today's summary - all totals
class TodaySummaryListView(generic.ListView):
    template_name = ''
    context_object_name = 'today_summary_list'
    model = TodayBookingView

    def get_queryset(self):
        return TodayBookingView.objects.all()


# creating a new booking
def add_booking_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                booking = Booking()
                booking.user_id = request_params.get('user_id')
                booking.start_date = request_params.get('start_date')
                booking.end_date = request_params.get('end_date')
                booking.facility_type = request_params.get('facility_type')
                booking.facility_id = request_params.get('facility_id')
                booking.hotel_id = request_params.get('hotel_id')
                booking.status = request_params.get('status')
                booking.confirmation_number = request_params.get('confirmation_number')
                booking.package_id = request_params.get('package_id')
                booking.booking_date = request_params.get('booking_date')
                booking.save()
                return http.HttpResponse(
                    json.dumps({'id': booking.booking_id, 'confirmation_number': booking.confirmation_number}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. booking not created")


# updating booking
def update_booking_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            booking = _update_ajax(Booking, request)
            return http.HttpResponse(
                json.dumps({'pk': booking.booking_id, 'confirmation_number': booking.confirmation_number, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting booking that was made
def delete_booking_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            booking = Booking.objects.get(pk=request.POST.get('pk'))
            booking_cn = booking.confirmation_number
            booking.delete()
            return http.HttpResponse(
                content='booking <strong>{}</strong> has been successfully deleted'.format(booking_cn), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# creating a new check in to track users facility usage
def tracking_check_in_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                check_in = UserTrackingMovements()
                check_in.facility_id = request_params.get('user_id')
                check_in.facility_id = request_params.get('location')
                check_in.facility_id = request_params.get('facility_id')
                check_in.facility_id = request_params.get('facility_type')
                check_in.status = request_params.get('status')
                check_in.save()

                return http.HttpResponse(json.dumps(
                    {'id': check_in.tracking_id, 'checked_in_facility': check_in.facility_id,
                     'status': check_in.status}), status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. Tracking Check in not created")


# Tracking - checkout from a facility
def tracking_check_out_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.method == 'POST' and request.is_ajax():
            try:
                check_out = _update_ajax(Booking, request)
                return http.HttpResponse(json.dumps({'pk': check_out.tracking_id, 'status': check_out.status, }),
                                         status=201)
            except DatabaseError as e:
                return http.HttpResponse(status=400, content='An error occurred while processing your request')
        return http.HttpResponse(status=400)


# Getting tracking trends - most used facilities
class MostUsedFacilityListView(generic.ListView):
    template_name = ''
    context_object_name = 'facilities_most_used_list'
    model = MostUsedFacilityView

    def get_queryset(self):
        return MostUsedFacilityView.objects.all()


# Getting tracking trends - least used facilities
class LeastUsedFacilityListView(generic.ListView):
    template_name = ''
    context_object_name = 'facilities_least_used_list'
    model = LeastUsedFacilityView

    def get_queryset(self):
        return LeastUsedFacilityView.objects.all()

# TODO
# Creating a new order
def add_order_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                order = Orders()
                order.order_id = request_params.get('order_id')
                order.order_time = request_params.get('order_time')
                order.order_status = request_params.get('order_status')
                order.menu_id = request_params.get('menu_id')
                order.paid = request_params.get('paid')
                order.created_by = request_params.get('created_by')
                order.created_on = request_params.get('created_on')
                order.save()
                return http.HttpResponse(
                    json.dumps({'id': order.order_id, 'order_status': order.order_status}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. booking not created")


# List all orders
class AllOrdersListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_orders_list'
    model = AllOrdersListView

    def get_queryset(self):
        return AllOrdersListView.objects.all()


# Update order, cancell or process
def update_order_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            order = _update_ajax(Orders, request)
            return http.HttpResponse(
                json.dumps({'pk': order.order_id, 'status': order.status, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# Creating  new food
def add_food_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                food = Food()
                food.food_id = request_params.get('food_id')
                food.food_type = request_params.get('food_type')
                food.name = request_params.get('food_name')
                food.quantity = request_params.get('quantity')
                food.metric = request_params.get('metric')
                food.created_on = request_params.get('created_on')
                food.save()
                return http.HttpResponse(
                    json.dumps({'id': food.food_id, 'food_id': food.food_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. food not created")


# List all food
class AllFoodListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_food_list'
    model = Food

    def get_queryset(self):
        return AllFoodListView.objects.all()


# updating food
def update_food_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            food = _update_ajax(Food, request)
            return http.HttpResponse(
                json.dumps({'pk': food.food_id, 'food_id': food.food_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting food
def delete_food_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            food = Food.objects.get(pk=request.POST.get('pk'))
            food_id = food.food_id
            food.delete()
            return http.HttpResponse(
                content='food <strong>{}</strong> has been successfully deleted'.format(food_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  new drink
def add_drink_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                drink = Drink()
                drink.drink_id = request_params.get('drink_id')
                drink.drink_type = request_params.get('drink_type')
                drink.name = request_params.get('drink_name')
                drink.quantity = request_params.get('quantity')
                drink.metric = request_params.get('metric')
                drink.created_on = request_params.get('created_on')
                drink.save()
                return http.HttpResponse(
                    json.dumps({'id': drink.drink_id, 'drink_id': drink.drink_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. drink not created")


# List all drinks
class AllDrinkListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_drink_list'
    model = Drink

    def get_queryset(self):
        return AllDrinkListView.objects.all()


# updating drink
def update_drink_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            drink = _update_ajax(Food, request)
            return http.HttpResponse(
                json.dumps({'pk': drink.drink_id, 'drink_id': drink.drink_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting drink
def delete_drink_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            drink = Drink.objects.get(pk=request.POST.get('pk'))
            drink_id = drink.drink_id
            drink.delete()
            return http.HttpResponse(
                content='drink <strong>{}</strong> has been successfully deleted'.format(drink_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


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
    model = Drink

    def get_queryset(self):
        return AllCommodityListView.objects.all()


# updating commodity
def update_commodity_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity = _update_ajax(Commodity, request)
            return http.HttpResponse(
                json.dumps({'pk': commodity.commodity_id, 'commodity_id': commodity.commodity_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting commodity
def delete_drink_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            commodity = Commodity.objects.get(pk=request.POST.get('pk'))
            commodity_id = commodity.commodity_id
            commodity.delete()
            return http.HttpResponse(
                content='commodity <strong>{}</strong> has been successfully deleted'.format(commodity_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new supplier
def add_supplier_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                supplier = Suppliers()
                supplier.supplier_id = request_params.get('supplier_id')
                supplier.supplier_name = request_params.get('supplier_name')
                supplier.supply_type = request_params.get('supplier_type')
                supplier.supply_item = request_params.get('supply_item')
                supplier.phone = request_params.get('supplier_phone')
                supplier.email = request_params.get('supplier_email')
                supplier.created_on = request_params.get('created_on')
                supplier.save()
                return http.HttpResponse(
                    json.dumps({'id': supplier.supplier_id, 'supplier_id': supplier.supplier_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all suppliers
class AllSuppliersListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_suppliers_list'
    model = Suppliers

    def get_queryset(self):
        return AllSuppliersListView.objects.all()


# updating suppliers
def update_supplier_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            supplier = _update_ajax(Suppliers, request)
            return http.HttpResponse(
                json.dumps({'pk': supplier.supplier_id, 'supplier_id': supplier.supplier_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting supplier
def delete_supplier_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            supplier = Suppliers.objects.get(pk=request.POST.get('pk'))
            supplier_id = supplier.supplier_id
            supplier.delete()
            return http.HttpResponse(
                content='supplier <strong>{}</strong> has been successfully deleted'.format(supplier_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new staff
def add_worker_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                worker = Workers()

                worker.worker_id = request_params.get('worker_id')
                worker.name = request_params.get('name')
                worker.phone = request_params.get('phone')
                worker.email = request_params.get('email')
                worker.id_number = request_params.get('id_number')
                worker.gender = request_params.get('gender')
                worker.staff_id = request_params.get('staff_id')
                worker.role = request_params.get('role')
                worker.shift = request_params.get('shift')
                worker.created_on = request_params.get('created_on')
                worker.save()
                return http.HttpResponse(
                    json.dumps({'id': worker.worker_id, 'worker_id': worker.worker_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all staff
class AllWorkersListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_workers_list'
    model = Workers

    def get_queryset(self):
        return AllWorkersListView.objects.all()


# updating staff
def update_worker_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            worker = _update_ajax(Workers, request)
            return http.HttpResponse(
                json.dumps({'pk': worker.worker_id, 'worker_id': worker.worker_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a staff
def delete_worker_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            worker = Workers.objects.get(pk=request.POST.get('pk'))
            worker_id = worker.worker_id
            worker.delete()
            return http.HttpResponse(
                content='staff <strong>{}</strong> has been successfully deleted'.format(worker_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  new laundry type costs
def add_laundry_type_cost_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                laundry = LaundryType()

                laundry.laundry_item_id = request_params.get('laundry_item_id')
                laundry.clothe_type = request_params.get('clothe_type')
                laundry.cost = request_params.get('cost')
                laundry.created_on = request_params('created_on')
                laundry.save()
                return http.HttpResponse(
                    json.dumps({'id': laundry.laundry_item_id, 'laundry_item_id': laundry.laundry_item_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all laundry types cost
class AllLaundryTypeCostListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_laundry_type_cost_list'
    model = LaundryType

    def get_queryset(self):
        return AllLaundryTypeCostListView.objects.all()


# updating laundry type costs
def update_laundry_type_cost_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            laundry = _update_ajax(LaundryType, request)
            return http.HttpResponse(
                json.dumps({'pk': laundry.laundry_item_id, 'laundry_item_id': laundry.laundry_item_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting laundry type cost
def delete_laundry_type_cost_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            laundry = LaundryType.objects.get(pk=request.POST.get('pk'))
            laundry_item_id = laundry.laundry_item_id
            laundry.delete()
            return http.HttpResponse(
                content='laundry type cost <strong>{}</strong> has been successfully deleted'.format(laundry_item_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new facility
def add_facility_type_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                facility = FacilityType()

                facility.facility_type_id = request_params.get('facility_type_id')
                facility.facility_type = request_params.get('facility_type')
                facility.created_on = request_params.get('created_on')
                facility.save()
                return http.HttpResponse(
                    json.dumps({'id': facility.facility_type_id, 'facility_type_id': facility.facility_type_id}),
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
                json.dumps({'pk': facility.facility_type_id, 'facility_type_id': facility.facility_type_id, }),
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
                facility = Facilities

                facility.facility_id = request_params.get('facility_id')
                facility.facility_number = request_params.get('facility_number')
                facility.facility_name = request_params.get('facility_name')
                facility.floor = request_params.get('floor')
                facility.facility_type = request_params.get('facility_type')
                facility.location = request_params.get('location')
                facility.capacity = request_params.get('facility_capacity')
                facility.created_on = request_params.get('created_on')
                facility.save()
                return http.HttpResponse(
                    json.dumps({'id': facility.facility_id, 'facility_id': facility.facility_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all Facility
class AllFacilityListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_facility_list'
    model = Facilities

    def get_queryset(self):
        return AllFacilityListView.objects.all()


# updating facility
def update_facility_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = _update_ajax(Facilities, request)
            return http.HttpResponse(
                json.dumps({'pk': facility.facility_id, 'facility_id': facility.facility_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a facility
def delete_facility_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = Facilities.objects.get(pk=request.POST.get('pk'))
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

                rate.rating_id = request_params.get('rating_id')
                rate.user_id = request_params.get('user_id')
                rate.rating = request_params.get('rating')
                rate.comment = request_params.get('comment')
                rate.created_on = request_params.get('created_on')

                rate.save()
                return http.HttpResponse(
                    json.dumps({'id': rate.rating_id, 'rating_id': rate.rating_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all ratings
class AllRatingsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_ratings_list'
    model = Facilities

    def get_queryset(self):
        return AllRatingsListView.objects.all()


# updating a rating
def update_rating_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            rate = _update_ajax(Ratings, request)
            return http.HttpResponse(
                json.dumps({'pk': rate.rating_id, 'rating_id': rate.rating_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting a rating
def delete_rating_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            rate = Ratings.objects.get(pk=request.POST.get('pk'))
            rating_id = rate.rating_id
            rate.delete()
            return http.HttpResponse(
                content='rating <strong>{}</strong> has been successfully deleted'.format(rating_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Creating  a new rating
def add_event_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                event = Events

                event.event_id = request_params.get('event_id')
                event.name = request_params.get('name')
                event.venue = request_params.get('venue')
                event.type = request_params.get('type')
                event.start_date = request_params.get('start_date')
                event.end_date = request_params.get('end_date')
                event.time = request_params.get('time')
                event.created_on = request_params.get('created_on')

                event.save()
                return http.HttpResponse(
                    json.dumps({'id': event.event_id, 'event_id': event.event_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all events
class AllEventsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_events_list'
    model = Events

    def get_queryset(self):
        return AllEventsListView.objects.all()


# updating an event
def update_event_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            event = _update_ajax(Events, request)
            return http.HttpResponse(
                json.dumps({'pk': event.event_id, 'event_id': event.event_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting an event
def delete_event_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            event = Events.objects.get(pk=request.POST.get('pk'))
            event_id = event.event_id
            event.delete()
            return http.HttpResponse(
                content='event <strong>{}</strong> has been successfully deleted'.format(event_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Assign cleaning of room
def add_room_cleaning_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                room = CleaningRoomView

                room.facility_id = request_params.get('facility_id')
                room.facility_type_id = request_params.get('facility_type_id')
                room.room_number = request_params.get('room_number')
                room.status = request_params.get('status')
                room.worker_id = request_params.get('worker_id')
                room.worker_name = request_params.get('worker_name')
                room.created_by = request_params.get('created_by')
                room.created_on = request_params.get('created_on')

                room.save()
                return http.HttpResponse(
                    json.dumps({'id': room.facility_id, 'facility_id': room.facility_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all room cleanings
class AllRoomCleaningsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_room_cleaning_list'
    model = Events

    def get_queryset(self):
        return AllRoomCleaningsListView.objects.all()


# updating room cleaning
def update_room_cleaning_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            room = _update_ajax(Events, request)
            return http.HttpResponse(
                json.dumps({'pk': room.facility_id, 'facility_id': room.facility_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting room cleaning
def delete_room_cleaning_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            room = CleaningRoomView.objects.get(pk=request.POST.get('pk'))
            facility_id = room.facility_id
            room.delete()
            return http.HttpResponse(
                content='room <strong>{}</strong> has been successfully deleted'.format(facility_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')


# Assign cleaning of a facility
def add_facility_cleaning_ajax(request, **kwargs):
    if request.method == 'POST':
        if request.is_ajax():
            request_params = request.POST.dict()
            print(request_params)

            try:
                facility = CleaningFacilityView

                facility.facility_id = request_params.get('facility_id')
                facility.facility_type_id = request_params.get('facility_type_id')
                facility.facility_number = request_params.get('facility_number')
                facility.status = request_params.get('status')
                facility.worker_id = request_params.get('worker_id')
                facility.worker_name = request_params.get('worker_name')
                facility.created_by = request_params.get('created_by')
                facility.created_on = request_params.get('created_on')

                facility.save()
                return http.HttpResponse(json.dumps({'id': facility.facility_id, 'facility_id': facility.facility_id}),
                    status=201)

            except DatabaseError as e:
                return http.HttpResponse(status=400, content="A problem occurred. commodity not created")


# List all facilities cleanings
class AllFacilityCleaningsListView(generic.ListView):
    template_name = ''
    context_object_name = 'all_facility_cleaning_list'
    model = Events

    def get_queryset(self):
        return AllFacilityCleaningsListView.objects.all()


# updating facility cleaning
def update_facility_cleaning_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = _update_ajax(Events, request)
            return http.HttpResponse(json.dumps({'pk': facility.facility_id, 'facility_id': facility.facility_id, }),
                status=201)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')
    return http.HttpResponse(status=400)


# deleting facility cleaning
def delete_facility_cleaning_ajax(request, **kwargs):
    if request.method == 'POST' and request.is_ajax():
        try:
            facility = CleaningFacilityView.objects.get(pk=request.POST.get('pk'))
            facility_id = facility.facility_id
            facility.delete()
            return http.HttpResponse(
                content='facility <strong>{}</strong> has been successfully deleted'.format(facility_id), status=200)
        except DatabaseError as e:
            return http.HttpResponse(status=400, content='An error occurred while processing your request')














