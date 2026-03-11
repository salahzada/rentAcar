from django.db import models


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.profile} | {self.car} | {self.status}"

    class Meta:
        db_table = "bookings"
        ordering = ["-created_at"]


class DeletedBooking(models.Model):
    CANCELLED_BY_CHOICES = [
        ('customer', 'Customer'),
        ('car_owner', 'Car Owner'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    original_booking_id = models.IntegerField()
    customer_username = models.CharField(max_length=150)
    customer_full_name = models.CharField(max_length=300, null=True, blank=True)
    car_brand = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    car_registration = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status_at_deletion = models.CharField(max_length=20)
    notes = models.TextField(null=True, blank=True)
    cancelled_by = models.CharField(max_length=20, choices=CANCELLED_BY_CHOICES, null=True, blank=True)
    deleted_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deleted_bookings'
    )
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[DELETED] Booking #{self.original_booking_id} — {self.customer_username} | {self.car_brand} {self.car_model} | {self.deleted_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        db_table = "deleted_bookings"
        ordering = ["-deleted_at"]
        verbose_name = "Deleted Booking"
        verbose_name_plural = "Deleted Bookings"