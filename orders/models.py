from django.db import models
from menu.models import Product
import uuid

class Order(models.Model):

    PAYMENT_METHOD = [
        ("NEQUI", "Nequi"),
        ("EFECTIVO", "Efectivo"),
        ("TARJETA", "Tarjeta"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("PREPARING", "En preparación"),
        ("READY", "Listo"),
        ("DELIVERED", "Entregado"),
    ]

    # Datos del cliente
    customer_name = models.CharField(max_length=120)
    customer_lastname = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)

    # Pago y estado
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    
    # Nota opcional
    note = models.TextField(blank=True, null=True)

    # Tracking
    tracking_code = models.CharField(max_length=10, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_name} {self.customer_lastname}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
