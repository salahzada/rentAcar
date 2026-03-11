from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'carBrand', 'carModel', 'carCategory', 'carYear', 'carKM',
            'carFuelType', 'bensinType', 'carType', 'karopkaType',
            'dailyRentPrice', 'carIdNumber', 'carRegistrationNumber',
            'carColor', 'carMotor', 'carSits', 'isPersonal'
        ]
        # profile is excluded — assigned automatically in view


class CarAdminForm(forms.ModelForm):
    """Admin/staff can also assign the car to any profile."""
    class Meta:
        model = Car
        fields = [
            'profile', 'carBrand', 'carModel', 'carCategory', 'carYear', 'carKM',
            'carFuelType', 'bensinType', 'carType', 'karopkaType',
            'dailyRentPrice', 'carIdNumber', 'carRegistrationNumber',
            'carColor', 'carMotor', 'carSits', 'isPersonal'
        ]