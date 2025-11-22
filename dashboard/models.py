from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Administrador"),
        ("BARISTA", "Barista"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="BARISTA")

    # -----------------------------------------------------
    # Propiedades útiles
    # -----------------------------------------------------
    @property
    def is_admin(self):
        return self.role == "ADMIN"

    @property
    def is_barista(self):
        return self.role == "BARISTA"

    # -----------------------------------------------------
    # Asegurar que un superusuario también sea ADMIN
    # -----------------------------------------------------
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "ADMIN"
        super().save(*args, **kwargs)
