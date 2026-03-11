from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Car
from .forms import CarForm, CarAdminForm


class CarAccessMixin(LoginRequiredMixin):

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


class CarListView(CarAccessMixin, ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return Car.objects.all().select_related('profile__user')

        if role == 'car_owner':
            return Car.objects.filter(profile=profile).select_related('profile__user')

        if role == 'customer':
            # Customers can browse all available cars
            return Car.objects.all().select_related('profile__user')

        return Car.objects.none()


class CarDetailView(CarAccessMixin, DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'


class CarCreateView(CarAccessMixin, CreateView):
    model = Car
    template_name = 'cars/car_form.html'
    success_url = reverse_lazy('cars:list')

    def dispatch(self, request, *args, **kwargs):
        role = self.get_role()
        if role == 'customer':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return CarAdminForm
        return CarForm

    def form_valid(self, form):
        if self.get_role() == 'car_owner':
            form.instance.profile = self.get_profile()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Add Car'
        return ctx


class CarUpdateView(CarAccessMixin, UpdateView):
    model = Car
    template_name = 'cars/car_form.html'
    success_url = reverse_lazy('cars:list')

    def dispatch(self, request, *args, **kwargs):
        role = self.get_role()
        if role == 'customer':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.get_role() in ('admin', 'staff'):
            return CarAdminForm
        return CarForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'car_owner' and obj.profile == profile:
            return obj

        raise PermissionDenied

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit Car'
        return ctx

class CarDeleteView(CarAccessMixin, DeleteView):
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('cars:list')
    context_object_name = 'car'

    def dispatch(self, request, *args, **kwargs):
        if self.get_role() == 'customer':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        role = self.get_role()
        profile = self.get_profile()

        if role in ('admin', 'staff'):
            return obj
        if role == 'car_owner' and obj.profile == profile:
            return obj

        raise PermissionDenied

    def form_valid(self, form):
        from .models import DeletedCar

        # self.object is already fetched by Django — use it directly
        car = self.object

        DeletedCar.objects.create(
            original_car_id=car.pk,
            carBrand=car.carBrand,
            carModel=car.carModel,
            carCategory=car.carCategory,
            carYear=car.carYear,
            carKM=car.carKM,
            carFuelType=car.carFuelType or '',
            bensinType=car.bensinType or '',
            carType=car.carType,
            karopkaType=car.karopkaType,
            dailyRentPrice=car.dailyRentPrice,
            carIdNumber=car.carIdNumber,
            carLocation=car.carLocation,
            carRegistrationNumber=car.carRegistrationNumber,
            carColor=car.carColor,
            carMotor=car.carMotor,
            carSits=car.carSits,
            isPersonal=car.isPersonal,
            owner_username=car.profile.user.username if car.profile else 'unknown',
            owner_full_name=car.profile.user.get_full_name() if car.profile else '',
            deleted_by=self.request.user,
        )

        # Now delete the actual car
        return super().form_valid(form)