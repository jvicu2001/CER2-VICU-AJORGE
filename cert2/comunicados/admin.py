from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import AdminEntidad

# Register your models here.
class AdminEntidadInline(admin.StackedInline):
    model = AdminEntidad
    can_delete = False
    verbose_name_plural = 'AdminEntidades'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AdminEntidadInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
