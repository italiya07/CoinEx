from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cryptocurrency,Profile, Tweet


class ProfileInline(admin.StackedInline):
    model=Profile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('id',)

    # Remove 'groups' and 'user_permissions' from filter_horizontal
    filter_horizontal = ()
    
    # Remove 'groups' from list_filter
    list_filter = ()
    
    # Exclude 'date_joined' from fieldsets
    fieldsets = (
        
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'date_joined', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    readonly_fields = ['date_joined']
    inlines=[ProfileInline]


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cryptocurrency)
admin.site.register(Tweet)


