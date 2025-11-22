from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from orders.models import Order
from menu.models import Product, Category
from .models import User
from django.http import HttpResponse

# ----------------------------------------
# LOGIN
# ----------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")

    if request.method == "POST":
        username = request.POST.get("usuario")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard_home")
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, "dashboard/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

# ----------------------------------------
# HOME (ADMIN)
# ----------------------------------------
def dashboard_home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")

    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    status_data_raw = (
        Order.objects.values("status")
        .annotate(count=Count("status"))
        .order_by()
    )

    status_labels = [item["status"] for item in status_data_raw]
    status_data = [item["count"] for item in status_data_raw]

    daily_raw = (
        Order.objects.extra({"date": "date(created_at)"})
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    daily_labels = [str(item["date"]) for item in daily_raw]
    daily_data = [item["count"] for item in daily_raw]

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "status_labels": status_labels,
        "status_data": status_data,
        "daily_labels": daily_labels,
        "daily_data": daily_data,
    }

    return render(request, "dashboard/home.html", context)

# ----------------------------------------
# BARISTAS (Las funciones permanecen igual)
# ----------------------------------------
def barista_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    baristas = User.objects.filter(role="BARISTA")
    return render(request, "dashboard/barista_list.html", {"baristas": baristas})

def barista_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    if request.method == "POST":
        username = request.POST.get("usuario")
        password = request.POST.get("password")
        if not username:
            messages.error(request, "El nombre de usuario es requerido.")
            return render(request, "dashboard/barista_create.html")
        if not password:
            messages.error(request, "La contraseña es requerida.")
            return render(request, "dashboard/barista_create.html")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nombre de usuario ya existe.")
            return render(request, "dashboard/barista_create.html")
        User.objects.create_user(
            username=username,
            password=password,
            role="BARISTA"
        )
        messages.success(request, "Barista creado correctamente.")
        return redirect("barista_list")
    return render(request, "dashboard/barista_create.html")

def barista_edit(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    barista = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        barista.username = request.POST.get("usuario")
        password = request.POST.get("password")
        if password:
            barista.set_password(password)
        barista.save()
        messages.success(request, "Barista actualizado correctamente.")
        return redirect("barista_list")
    return render(request, "dashboard/barista_edit.html", {"barista": barista})

def barista_delete(request, user_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    barista = get_object_or_404(User, id=user_id, role="BARISTA")
    if request.method == "POST":
        barista.delete()
        messages.success(request, "Barista eliminado correctamente.")
        return redirect("barista_list")
    return render(request, "dashboard/barista_delete.html", {"barista": barista})

# ----------------------------------------
# PRODUCTOS (Las funciones permanecen igual)
# ----------------------------------------
def product_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, "dashboard/product_list.html", context)

def product_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")
        if not name or not price or not category_id:
            messages.error(request, "Todos los campos son requeridos.")
            categories = Category.objects.all()
            return render(request, "dashboard/product_create.html", {"categories": categories})
        category = get_object_or_404(Category, id=category_id)
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )
        messages.success(request, "Producto creado correctamente.")
        return redirect("product_list")
    categories = Category.objects.all()
    return render(request, "dashboard/product_create.html", {"categories": categories})

def product_edit(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        category_id = request.POST.get("category")
        product.category = get_object_or_404(Category, id=category_id)
        if request.FILES.get("image"):
            product.image = request.FILES.get("image")
        product.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect("product_list")
    categories = Category.objects.all()
    context = {
        "product": product,
        "categories": categories,
    }
    return render(request, "dashboard/product_edit.html", context)

def product_delete(request, product_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("product_list")
    return render(request, "dashboard/product_delete.html", {"product": product})

# ----------------------------------------
# CATEGORÍAS (Las funciones permanecen igual)
# ----------------------------------------
def category_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    categories = Category.objects.all()
    return render(request, "dashboard/category_list.html", {"categories": categories})

def category_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            messages.error(request, "El nombre de la categoría es requerido.")
            return render(request, "dashboard/category_create.html")
        Category.objects.create(name=name)
        messages.success(request, "Categoría creada correctamente.")
        return redirect("category_list")
    return render(request, "dashboard/category_create.html")

def category_edit(request, category_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Categoría actualizada correctamente.")
        return redirect("category_list")
    return render(request, "dashboard/category_edit.html", {"category": category})

def category_delete(request, category_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role != "ADMIN":
        return render(request, "dashboard/acceso_denegado.html")
    category = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Categoría eliminada correctamente.")
        return redirect("category_list")
    return render(request, "dashboard/category_delete.html", {"category": category})

# ----------------------------------------
# PEDIDOS
# ----------------------------------------
def pedidos_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role not in ["ADMIN", "BARISTA"]:
        return render(request, "dashboard/acceso_denegado.html")
    pedidos = Order.objects.all().order_by('-created_at')
    context = {
        "pedidos": pedidos,
    }
    return render(request, "dashboard/pedidos_list.html", context)

def pedido_detalle(request, order_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role not in ["ADMIN", "BARISTA"]:
        return render(request, "dashboard/acceso_denegado.html")
    pedido = get_object_or_404(Order, id=order_id)
    # Lógica para imprimir solo si el pedido está entregado
    imprimir = request.GET.get("imprimir", "") == "1"
    if imprimir and pedido.status == "DELIVERED":
        return imprimir_factura(request, pedido)
    context = {
        "pedido": pedido,
    }
    return render(request, "dashboard/pedido_detalle.html", context)

def cambiar_estado_pedido(request, order_id, nuevo_estado):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.user.role not in ["ADMIN", "BARISTA"]:
        return render(request, "dashboard/acceso_denegado.html")
    pedido = get_object_or_404(Order, id=order_id)
    # Solo acepta los estados válidos en inglés (como en el modelo)
    estados_validos = ['PENDING', 'PREPARING', 'READY', 'DELIVERED']
    estado_upper = nuevo_estado.upper()
    if estado_upper in estados_validos:
        pedido.status = estado_upper
        pedido.save()
        messages.success(request, f"Estado del pedido actualizado a {pedido.get_status_display()}.")
        if estado_upper == "DELIVERED":
            # Redirige con parámetro para imprimir
            return redirect(f"/dashboard/pedidos/{pedido.id}/?imprimir=1")
    else:
        messages.error(request, "Estado no válido.")
    return redirect("pedido_detalle", order_id=order_id)

def imprimir_factura(request, pedido):
    """Devuelve una factura simple como HTML imprimible."""
    productos = pedido.items.all()
    total = sum(item.product.price * item.quantity for item in productos)
    factura_html = f"""
    <html>
    <head>
    <title>Factura Pedido #{pedido.id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin:2rem; }}
        h2 {{ color: #8b6f47; }}
        table {{ border-collapse: collapse; width: 60%; margin-top:1rem; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f2e7d6; }}
    </style>
    </head>
    <body>
    <h2>Factura - Pedido #{pedido.id}</h2>
    <p><b>Fecha:</b> {pedido.created_at.strftime('%Y-%m-%d %H:%M')}</p>
    <p><b>Cliente:</b> {pedido.customer_name} {pedido.customer_lastname}</p>
    <p><b>Teléfono:</b> {pedido.customer_phone}</p>
    <p><b>Método de pago:</b> {pedido.get_payment_method_display()}</p>
    <table>
        <tr>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Subtotal</th>
        </tr>
        {" ".join([f"<tr><td>{item.product.name}</td><td>{item.quantity}</td><td>${item.product.price*item.quantity:.2f}</td></tr>" for item in productos])}
        <tr>
            <th colspan="2" style="text-align:right;">Total:</th>
            <th>${total:.2f}</th>
        </tr>
    </table>
    <script>window.print()</script>
    </body>
    </html>
    """
    return HttpResponse(factura_html)
