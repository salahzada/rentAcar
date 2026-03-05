from django.contrib import admin
from unfold.admin import ModelAdmin  # replace django.contrib.admin.ModelAdmin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("id", "profile", "car", "status", "start_date", "end_date", "total_price", "created_at")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("profile__name", "profile__personal_id", "car__carBrand", "car__carModel")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)