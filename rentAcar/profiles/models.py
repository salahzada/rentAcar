from django.db import models
from django.core.exceptions import ValidationError


class Profile(models.Model):
    ROLE_CHOICES = [
        ('car_owner', 'Car Owner'),
        ('customer', 'Customer'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    personal_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def clean(self):
        if not self.user.is_staff and not self.user.is_superuser:
            if not self.role:
                raise ValidationError({'role': 'Role is required for customers and car owners.'})
            if not self.pincode:
                raise ValidationError({'pincode': 'Pincode is required for customers and car owners.'})
            if not self.personal_id:
                raise ValidationError({'personal_id': 'Personal ID is required for customers and car owners.'})

    def __str__(self):
        return f"{self.user.username} - {self.role if self.role else 'Staff/Admin'}"

    class Meta:
        db_table = "profiles"