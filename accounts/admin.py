from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "active",
        "staff",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
    )
    ordering = ("email",)
    filter_horizontal = ()
    search_fields = ('email',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('staff','admin',)}),
    )
    
admin.site.register(User, UserAdmin)