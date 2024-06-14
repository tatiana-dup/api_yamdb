from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MdbUser


UserAdmin.fieldsets += (
    ('Дополнительные поля', {'fields': ('bio', 'role')}),
)
admin.site.register(MdbUser, UserAdmin)
