from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('date_joined',)

    # Remove 'groups' and 'user_permissions' from filter_horizontal
    filter_horizontal = ()
    
    # Remove 'groups' from list_filter
    list_filter = ()


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
