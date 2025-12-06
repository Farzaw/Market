from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from account.models import User, Employee, CashSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'role', 'is_active')
    list_display_links = ('email',)
    list_filter = ('role',)
    readonly_fields = ('created_at',)
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('created_at', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'position_id', 'user')
    list_display_links = ('first_name',)


@admin.register(CashSession)
class CashSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cashier', 'start_time', 'money_start', 'end_time', 'money_end')
    list_display_links = ('cashier',)
