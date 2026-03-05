from django.db.models.signals import post_save
from django.contrib.auth.models import User as AuthUser, Permission
from django.dispatch import receiver
from .models import Profile


def assign_staff_permissions(user):
    # get all permissions for auth.user, profiles, cars, booking models
    staff_permissions = Permission.objects.filter(
        content_type__app_label__in=['auth', 'profiles', 'cars', 'bookings']
    ).exclude(
        # staff cannot add/change/delete other staff or superusers
        codename__in=[
            'add_permission', 'change_permission', 'delete_permission',
        ]
    )
    user.user_permissions.set(staff_permissions)


@receiver(post_save, sender=AuthUser)
def create_or_save_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff and not instance.is_superuser:
            assign_staff_permissions(instance)
        elif not instance.is_superuser and not instance.is_staff:
            Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()