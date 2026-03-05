from django.contrib import admin
from unfold.admin import ModelAdmin  # replace django.contrib.admin.ModelAdmin
from .models import Car


@admin.register(Car)
class CarAdmin(ModelAdmin):
    list_display = ("id", "carBrand", "carModel", "carCategory", "carYear", "carKM", "carFuelType", "profile")
    list_filter = ("carBrand", "carCategory", "carFuelType", "carYear")
    search_fields = ("carBrand", "carModel", "profile__name", "profile__personal_id")
    ordering = ("-carYear",)