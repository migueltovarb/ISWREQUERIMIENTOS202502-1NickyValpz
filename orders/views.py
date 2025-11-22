from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from .models import Order, OrderItem
from .utils import generar_factura_pdf


def crear_pedido(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        metodo = request.POST.get("metodo_pago")

        if not nombre:
            messages.error(request, "Debes ingresar un nombre.")
            return redirect("realizar_pedido")

        order = Order.objects.create(
            customer_name=nombre,
            payment_method=metodo,
            status="pendiente",
        )

        cart = request.session.get("cart", {})

        for product_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )

        request.session["cart"] = {}
        return redirect("tracking", tracking_code=order.tracking_code)

    return redirect("menu_home")


def pedidos_list(request):
    user = request.user
    if user.is_barista:
        orders = Order.objects.all().order_by("-created_at")
    else:
        orders = []

    estado = request.GET.get("estado")
    if estado and estado != "todos":
        orders = orders.filter(status=estado)

    return render(request, "orders/pedidos_list.html", {"orders": orders})


def pedido_detalle(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, "orders/pedido_detalle.html", {
        "order": order,
        "items": items,
    })


# ----------------------------------------
# ⭐ CAMBIAR ESTADO — FIX COMPLETO
# ----------------------------------------
def cambiar_estado_pedido(request, order_id, nuevo_estado):
    order = get_object_or_404(Order, id=order_id)

    if not request.user.is_barista and not request.user.is_admin:
        return render(request, "dashboard/acceso_denegado.html")

    # Validar estados válidos
    estados_validos = ["pendiente", "preparacion", "listo", "entregado"]

    if nuevo_estado not in estados_validos:
        messages.error(request, "Estado inválido.")
        return redirect("pedido_detalle", order_id=order.id)

    # Cambiar estado
    order.status = nuevo_estado
    order.save()

    # Si se entregó → generar la factura en PDF automáticamente
    if nuevo_estado == "entregado":
        pdf = generar_factura_pdf(order)
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="factura.pdf"'
        return response

    messages.success(request, f"Estado actualizado a {nuevo_estado.capitalize()}.")
    return redirect("pedido_detalle", order_id=order.id)


def tracking(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    items = OrderItem.objects.filter(order=order)

    return render(request, "orders/tracking.html", {
        "order": order,
        "items": items,
    })
