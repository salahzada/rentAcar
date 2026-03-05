from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin, StackedInline
from .models import Profile


class ProfileInline(StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj and not obj.is_staff and not obj.is_superuser:
            formset.form.base_fields['role'].required = True
            formset.form.base_fields['pincode'].required = True
            formset.form.base_fields['personal_id'].required = True
        return formset


class CustomUserAdmin(ModelAdmin, UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            if not request.user.is_superuser:
                return (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
                    }),
                )
            return self.add_fieldsets
        if obj.is_superuser or obj.is_staff:
            return self.fieldsets
        return (
            (None, {'fields': ('username', 'password')}),
            ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Status', {'fields': ('is_active',)}),
        )

    def get_inline_instances(self, request, obj=None):
        if not obj or obj.is_superuser or obj.is_staff:
            return []
        return super().get_inline_instances(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.is_superuser and obj.pk != request.user.pk:
                return False
            if not request.user.is_superuser and (obj.is_staff or obj.is_superuser):
                return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and (obj.is_staff or obj.is_superuser) and not request.user.is_superuser:
            return False
        if obj and obj.is_superuser and obj.pk != request.user.pk:
            return False
        return super().has_delete_permission(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_staff=False, is_superuser=False) | qs.filter(pk=request.user.pk)
        return qs

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     return form

    def get_role(self, obj):
        if obj.is_superuser:
            return 'ADMIN'
        if obj.is_staff:
            return 'STAFF'
        if hasattr(obj, 'profile') and obj.profile.role:
            return obj.profile.role.replace('_', ' ').title()
        return '-'
    get_role.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)