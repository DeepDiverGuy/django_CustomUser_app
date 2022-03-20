from .models import user

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# REGISTER your MODELS here.



class CustomUserAdmin(UserAdmin):
    # Customized Admin Interface for the custom User model
    
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'temp_email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin 
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'uuid_value', 'email', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(user, CustomUserAdmin)