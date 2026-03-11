from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.instance_pk = kwargs.get('instance').pk if kwargs.get('instance') else None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        car = cleaned_data.get('car')

        if start and end:
            if end <= start:
                raise forms.ValidationError('End date must be after start date.')

        if start and end and car:
            overlapping = Booking.objects.filter(
                car=car,
                start_date__lt=end,
                end_date__gt=start,
            ).exclude(status='cancelled')

            if self.instance_pk:
                overlapping = overlapping.exclude(pk=self.instance_pk)

            if overlapping.exists():
                raise forms.ValidationError(
                    f'This car is already booked between {start.strftime("%Y-%m-%d %H:%M")} '
                    f'and {end.strftime("%Y-%m-%d %H:%M")}. Please choose different dates.'
                )

        return cleaned_data


class BookingAdminForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['profile', 'car', 'start_date', 'end_date', 'status',
                  'total_price', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date':   forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }