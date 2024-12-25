from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ["id","name","email", "phone", "created", "modified", "image", "is_admin", "is_staff", "is_superuser", "is_active"]
    list_filter = ("is_admin", "is_active")

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("image",'email', 'name', 'phone', 'password1', 'password2'),
        }),
    )

    fieldsets=(
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name", "phone", "image")}),
        ("Permissions", {"fields": ("is_admin",)})
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)
