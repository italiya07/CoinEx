from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cryptocurrency, ContactUs, Transaction, NFT
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("id",)

    # Remove 'groups' and 'user_permissions' from filter_horizontal
    filter_horizontal = ()

    # Remove 'groups' from list_filter
    list_filter = ()

    # Exclude 'date_joined' from fieldsets
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "date_joined",
                    "password",
                    "id_or_photo",
                    "preview",
                )
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    readonly_fields = ["date_joined", "preview"]

    @admin.display
    def preview(self, obj):
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" style="max-width: 700px;"></a>',
            obj.id_or_photo.url,
            obj.id_or_photo.url,
        )


# Register the CustomUser model with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cryptocurrency)
admin.site.register(ContactUs)
admin.site.register(Transaction)
admin.site.register(NFT)
