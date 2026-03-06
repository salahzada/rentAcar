from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'start_date', 'end_date', 'pickup_location', 'dropoff_location', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end   = cleaned_data.get('end_date')
        if start and end and end <= start:
            raise forms.ValidationError('End date must be after start date.')
        return cleaned_data


class BookingAdminForm(forms.ModelForm):
    """Extended form for admin/staff — they can also set status, total_price, and profile."""
    class Meta:
        model = Booking
        fields = ['profile', 'car', 'start_date', 'end_date', 'status',
                  'total_price', 'pickup_location', 'dropoff_location', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }