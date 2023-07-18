from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "country",
        "active",
        "staff",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
        "country",
    )
    ordering = ("email",)
    filter_horizontal = ()
    search_fields = ('email', 'username', 'first_name', 'last_name', 'country')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'country', 'profile_image', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name', 'country', 'profile_image', 'password')}),
        ('Permissions', {'fields': ('staff','admin',)}),
    )
    
admin.site.register(User, UserAdmin)
