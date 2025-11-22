from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Columnas visibles en la tabla de usuarios
    list_display = ("username", "is_staff", "is_superuser")

    # Filtros laterales
    list_filter = ("is_staff", "is_superuser")

    # Campos que aparecen al editar un usuario
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Rol dentro del sistema", {"fields": ("role",)}),
    )

    # Campos que aparecen al crear un usuario desde el admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Rol dentro del sistema", {"fields": ("role",)}),
    )
