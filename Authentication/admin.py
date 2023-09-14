from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CusUser


# Register your models here.
class InfUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_status', 'is_superuser', 'is_verified',
        'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'artist', 'password')}),
        ('Personal Info',
         {'fields': ('first_name', 'last_name', 'avatar', 'cover_image', 'bio', 'short_bio', 'phone', 'gender', 'address', 'birthday')}),
        ('Permissions',
         {'fields': ('is_active', 'is_status', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'gender', 'password1', 'password2')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(CusUser, InfUserAdmin)
admin.site.unregister(Group)
