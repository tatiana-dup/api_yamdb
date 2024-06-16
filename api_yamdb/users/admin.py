from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MdbUser


@admin.register(MdbUser)
class MdbUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name', 'role',
                    'is_staff')

    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Информация о пользователе', {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'role')}),
        ('Разрешения', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
