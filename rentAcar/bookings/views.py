from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import Booking, DeletedBooking
from .forms import BookingForm, BookingAdminForm
from cars.models import Car
import json
from datetime import timedelta


class BookingAccessMixin(LoginRequiredMixin):

    def get_role(self):
        user = self.request.user
        if user.is_superuser:
            return 'admin'
        if user.is_staff:
            return 'staff'
        try:
            return user.profile.role
        except Exception:
            return None

    def get_profile(self):
        try:
            return self.request.user.profile
        except Exception:
            return None


class BookingListView(BookingAccessMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        role = self.get_role()
        profile = self.get_profile()
        status_filter = self.request.GET.get('status', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')

        if role in ('admin', 'staff'):
            qs = Booking.objects.all().select_related('profile__user', 'car')
        elif role == 'car_owner':
            qs = Booking.objects.filter(car__profile=profile).select_related('profile__user', 'car')
        elif role == 'customer':
            qs = Booking.objects.filter(profile=profile).select_related('car')
        else:
            return Booking.objects.none()

        if status_filter in ('pending', 'confirmed', 'cancelled'):
            qs = qs.filter(status=status_filter)

        if date_from:
            qs = qs.filter(start_date__gte=date_from)

        if date_to:
            qs = qs.filter(end_date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['date_from'] = self.request.GET.get('date_from', '')
        ctx['date_to'] = self.request.GET.get('date_to', '')
        ctx['role'] = self.get_role()
        return ctx


class BookingDetailView(BookingAccessMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'car_owner' and obj.car.profile == profile:
            return obj
        if role == 'customer' and obj.profile == profile:
            return obj

        raise PermissionDenied


class BookingCreateView(BookingAccessMixin, CreateView):
    model = Booking
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:list')

    def dispatch(self, request, *args, **kwargs):
        if self.get_role() == 'car_owner':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return BookingAdminForm
        return BookingForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        car_id = self.kwargs.get('car_id')
        if car_id and 'car' in form.fields:
            form.fields['car'].initial = car_id
            form.fields['car'].widget.attrs['readonly'] = True
        return form

    def form_valid(self, form):
        role = self.get_role()
        if role == 'customer':
            form.instance.profile = self.get_profile()
            form.instance.status = 'pending'
            start = form.cleaned_data.get('start_date')
            end = form.cleaned_data.get('end_date')
            car = form.cleaned_data.get('car')
            if start and end and car:
                days = max((end - start).days, 1)
                form.instance.total_price = days * car.dailyRentPrice
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create Booking'
        car_id = self.kwargs.get('car_id')
        if car_id:
            car = get_object_or_404(Car, pk=car_id)
            ctx['selected_car'] = car

            booked_ranges = Booking.objects.filter(
                car=car,
            ).exclude(status='cancelled').values_list('start_date', 'end_date')

            disabled_dates = []
            for start, end in booked_ranges:
                current = start
                while current <= end:
                    disabled_dates.append(current.strftime('%Y-%m-%d'))
                    current += timedelta(days=1)

            ctx['disabled_dates'] = json.dumps(disabled_dates)
        return ctx


class BookingUpdateView(BookingAccessMixin, UpdateView):
    model = Booking
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'customer' and obj.profile == profile:
            if obj.status == 'pending':
                raise PermissionDenied
            return obj

        raise PermissionDenied

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return BookingAdminForm
        return BookingForm

    def form_valid(self, form):
        if self.get_role() == 'customer':
            start = form.cleaned_data.get('start_date')
            end = form.cleaned_data.get('end_date')
            car = form.cleaned_data.get('car')
            if start and end and car:
                days = max((end - start).days, 1)
                form.instance.total_price = days * car.dailyRentPrice
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit Booking'
        return ctx


class BookingConfirmView(BookingAccessMixin, View):

    def post(self, request, pk):
        role = self.get_role()
        profile = self.get_profile()

        if role not in ('car_owner', 'admin', 'staff'):
            raise PermissionDenied

        booking = get_object_or_404(Booking, pk=pk)

        if role == 'car_owner' and booking.car.profile != profile:
            raise PermissionDenied

        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()

        return redirect('bookings:list')


class BookingCancelView(BookingAccessMixin, View):

    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        self._check_permission(request, booking)
        return render(request, 'bookings/booking_confirm_cancel.html', {'booking': booking})

    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            cancelled_by = role
        elif role == 'customer' and booking.profile == profile:
            if booking.status not in ('pending', 'confirmed'):
                raise PermissionDenied
            cancelled_by = 'customer'
        elif role == 'car_owner' and booking.car.profile == profile and booking.status == 'pending':
            cancelled_by = 'car_owner'
        else:
            raise PermissionDenied

        DeletedBooking.objects.create(
            original_booking_id=booking.pk,
            customer_username=booking.profile.user.username,
            customer_full_name=booking.profile.user.get_full_name(),
            car_brand=booking.car.carBrand,
            car_model=booking.car.carModel,
            car_year=booking.car.carYear,
            car_registration=booking.car.carRegistrationNumber,
            start_date=booking.start_date,
            end_date=booking.end_date,
            total_price=booking.total_price,
            status_at_deletion=booking.status,
            notes=booking.notes,
            cancelled_by=cancelled_by,
            deleted_by=request.user,
        )

        booking.status = 'cancelled'
        booking.save()

        return redirect('bookings:list')

    def _check_permission(self, request, booking):
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return
        if role == 'customer' and booking.profile == profile and booking.status in ('pending', 'confirmed'):
            return
        if role == 'car_owner' and booking.car.profile == profile and booking.status == 'pending':
            return

        raise PermissionDenied


class BookingDeleteView(BookingAccessMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:list')
    context_object_name = 'booking'

    def dispatch(self, request, *args, **kwargs):
        if self.get_role() not in ('admin', 'staff'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        booking = self.object
        DeletedBooking.objects.create(
            original_booking_id=booking.pk,
            customer_username=booking.profile.user.username,
            customer_full_name=booking.profile.user.get_full_name(),
            car_brand=booking.car.carBrand,
            car_model=booking.car.carModel,
            car_year=booking.car.carYear,
            car_registration=booking.car.carRegistrationNumber,
            start_date=booking.start_date,
            end_date=booking.end_date,
            total_price=booking.total_price,
            status_at_deletion=booking.status,
            notes=booking.notes,
            cancelled_by='admin',
            deleted_by=self.request.user,
        )
        return super().form_valid(form)