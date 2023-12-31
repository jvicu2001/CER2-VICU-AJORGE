from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import AdminEntidad, Comunicado, Entidad

# Register your models here.
admin.site.register(Entidad)


@admin.register(Comunicado)
class ComunicadoAdmin(admin.ModelAdmin):
    
    # Excluir campos autocompletados de ser listados si es que no es superusuario
    def get_exclude(self, request: HttpRequest, obj: Any | None = ...) -> Any:
        if not request.user.is_superuser:
            return ('publicado_por', 'modificado_por', 'fecha_publicacion', 'entidad', )
        return None

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        # Si no es superusuario, se asigna el usuario actual como publicado_por, y se asigna la entidad del usuario
        if not request.user.is_superuser:
            if not change:
                obj.publicado_por = request.user
                obj.entidad = request.user.adminentidad.entidad
            
            # Si se está modificando, se asigna el usuario actual como modificado_por
            else:
                obj.modificado_por = request.user
        super().save_model(request, obj, form, change)

    # No permitir que se eliminen comunicados de otras entidades
    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        if not request.user.is_superuser:
            if obj.entidad is not request.user.adminentidad.entidad:
                return
        return super().delete_model(request, obj)

    # Modifica el queryset para que solo se muestren los comunicados de la entidad correspondiente
    # https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_queryset
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super(ComunicadoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(entidad=request.user.adminentidad.entidad)

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
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
