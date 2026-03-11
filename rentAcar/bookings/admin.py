from django.contrib import admin
from django.db.models import Count
from .models import Booking, DeletedBooking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'car', 'start_date', 'end_date', 'status', 'total_price']
    list_filter = ['status']


@admin.register(DeletedBooking)
class DeletedBookingAdmin(admin.ModelAdmin):
    list_display = [
        'original_booking_id', 'customer_username', 'car_brand', 'car_model',
        'start_date', 'end_date', 'status_at_deletion', 'cancelled_by',
        'deleted_by', 'deleted_at'
    ]
    list_filter = ['cancelled_by', 'status_at_deletion']
    readonly_fields = [
        'original_booking_id', 'customer_username', 'customer_full_name',
        'car_brand', 'car_model', 'car_year', 'car_registration',
        'start_date', 'end_date', 'total_price', 'status_at_deletion',
        'notes',
        'cancelled_by', 'deleted_by', 'deleted_at'
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        stats = (
            DeletedBooking.objects
            .values('cancelled_by', 'customer_username')
            .annotate(total=Count('id'))
            .order_by('customer_username')
        )
        extra_context = extra_context or {}
        extra_context['cancellation_stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)