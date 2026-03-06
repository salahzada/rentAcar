from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Booking
from .forms import BookingForm, BookingAdminForm


class RoleCheckMixin(LoginRequiredMixin):
    """Resolves the current user's role."""

    def get_role(self):
        user = self.request.user
        if user.is_superuser:
            return 'admin'
        if user.is_staff:
            return 'staff'
        try:
            return user.profile.role  # 'car_owner' or 'customer'
        except Exception:
            return None

    def get_profile(self):
        try:
            return self.request.user.profile
        except Exception:
            return None


class BookingListView(RoleCheckMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return Booking.objects.all().select_related('profile__user', 'car')

        if role == 'car_owner':
            # Only bookings for cars that belong to this owner's profile
            return Booking.objects.filter(
                car__profile=profile
            ).select_related('profile__user', 'car')

        if role == 'customer':
            # Only own bookings
            return Booking.objects.filter(
                profile=profile
            ).select_related('car')

        return Booking.objects.none()


class BookingDetailView(RoleCheckMixin, DetailView):
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


class BookingCreateView(RoleCheckMixin, CreateView):
    model = Booking
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:list')

    def dispatch(self, request, *args, **kwargs):
        # Car owners cannot create bookings
        if self.get_role() == 'car_owner':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return BookingAdminForm
        return BookingForm

    def form_valid(self, form):
        role = self.get_role()
        if role == 'customer':
            # Auto-assign booking to the customer's own profile
            form.instance.profile = self.get_profile()
            # Auto-calculate total price based on days * daily rate
            start = form.cleaned_data.get('start_date')
            end   = form.cleaned_data.get('end_date')
            car   = form.cleaned_data.get('car')
            if start and end and car:
                days = max((end - start).days, 1)
                form.instance.total_price = days * car.dailyRentPrice
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


class BookingUpdateView(RoleCheckMixin, UpdateView):
    model = Booking
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:list')

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return BookingAdminForm
        return BookingForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'customer' and obj.profile == profile:
            return obj
        # car_owner and unauthorized customer → denied
        raise PermissionDenied

    def form_valid(self, form):
        role = self.get_role()
        if role == 'customer':
            # Recalculate price if dates or car changed
            start = form.cleaned_data.get('start_date')
            end   = form.cleaned_data.get('end_date')
            car   = form.cleaned_data.get('car')
            if start and end and car:
                days = max((end - start).days, 1)
                form.instance.total_price = days * car.dailyRentPrice
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class BookingDeleteView(RoleCheckMixin, DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('bookings:list')
    context_object_name = 'booking'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'customer' and obj.profile == profile:
            return obj

        raise PermissionDenied