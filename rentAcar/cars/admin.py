from django.contrib import admin
from unfold.admin import ModelAdmin  # replace django.contrib.admin.ModelAdmin
from .models import Car, DeletedCar


@admin.register(Car)
class CarAdmin(ModelAdmin):
    list_display = ("id", "carBrand", "carModel", "carCategory", "carYear", "carKM", "carFuelType", "profile")
    list_filter = ("carBrand", "carCategory", "carFuelType", "carYear",'carLocation')
    search_fields = ("carBrand", "carModel", "profile__name", "profile__personal_id")
    ordering = ("-carYear",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'profile':
            from profiles.models import Profile
            kwargs['queryset'] = Profile.objects.filter(role='car_owner')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(DeletedCar)
class DeletedCarAdmin(admin.ModelAdmin):
    list_display = [
        'original_car_id', 'carBrand', 'carModel', 'carYear',
        'owner_username', 'deleted_by', 'deleted_at'
    ]
    readonly_fields = [
        'original_car_id', 'carBrand', 'carModel', 'carCategory',
        'carYear', 'carKM', 'carFuelType', 'bensinType', 'carType',
        'karopkaType', 'dailyRentPrice', 'carLocation','carIdNumber', 'carRegistrationNumber',
        'carColor', 'carMotor', 'carSits', 'isPersonal',
        'owner_username', 'owner_full_name', 'deleted_at', 'deleted_by'
    ]
    # Nobody can add or delete from this table through admin — it's purely a backup log
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False