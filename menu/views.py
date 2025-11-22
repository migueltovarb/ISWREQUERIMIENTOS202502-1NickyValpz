from django.shortcuts import render, get_object_or_404, redirect
from menu.models import Category, Product
from orders.models import Order, OrderItem
from django.contrib import messages

# ---------------------------
# helpers para la bandeja
# ---------------------------
def _get_cart(request):
    cart = request.session.get('cart', {})
    return cart

def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

# ---------------------------
# vistas públicas
# ---------------------------

def menu_home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'menu/home.html', {
        'categories': categories,
        'products': products,
    })

def menu_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'menu/category.html', {
        'category': category,
        'products': products,
    })

def menu_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'menu/product_detail.html', {
        'product': product,
    })

# ---------------------------
# BANDEJA (CARRITO EN SESIÓN)
# ---------------------------

def agregar_a_bandeja(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = _get_cart(request)

    product_id_str = str(product.id)
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    _save_cart(request, cart)
    messages.success(request, f'{product.name} se agregó a la bandeja.')
    return redirect('bandeja')

def eliminar_de_bandeja(request, product_id):
    cart = _get_cart(request)
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        _save_cart(request, cart)
        messages.success(request, 'Producto eliminado de la bandeja.')

    return redirect('bandeja')

def vaciar_bandeja(request):
    _save_cart(request, {})
    messages.info(request, 'Bandeja vaciada.')
    return redirect('bandeja')

def bandeja_view(request):
    cart = _get_cart(request)
    items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'menu/bandeja.html', {
        'items': items,
        'total': total,
    })

# ---------------------------
# REALIZAR PEDIDO
# ---------------------------

def realizar_pedido(request):
    cart = _get_cart(request)
    if not cart:
        messages.error(request, 'Tu bandeja está vacía.')
        return redirect('menu_home')

    # construir resumen para mostrar
    items = []
    total = 0
    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_lastname = request.POST.get('customer_lastname')
        customer_phone = request.POST.get('customer_phone')
        payment_method = request.POST.get('payment_method')
        note = request.POST.get('note', '')

        if not all([customer_name, customer_lastname, customer_phone, payment_method]):
            messages.error(request, 'Todos los campos obligatorios deben estar llenos.')
            return redirect('realizar_pedido')

        # crear el pedido
        order = Order.objects.create(
            customer_name=customer_name,
            customer_lastname=customer_lastname,
            customer_phone=customer_phone,
            payment_method=payment_method,
            note=note
        )

        # crear los items del pedido
        for product_id_str, quantity in cart.items():
            product = get_object_or_404(Product, id=int(product_id_str))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        # vaciar bandeja
        _save_cart(request, {})

        # ---- HISTORIAL EN SESIÓN ----
        if 'order_history' not in request.session:
            request.session['order_history'] = []
        historial = request.session['order_history']
        if order.tracking_code not in historial:
            historial.append(order.tracking_code)
        request.session['order_history'] = historial
        request.session.modified = True
        # ---- FIN HISTORIAL ----

        messages.success(request, 'Tu pedido ha sido creado.')
        return redirect('tracking_view', tracking_code=order.tracking_code)

    return render(request, 'menu/realizar_pedido.html', {
        'items': items,
        'total': total,
    })

def tracking_view(request, tracking_code):
    order = get_object_or_404(Order, tracking_code=tracking_code)
    return render(request, 'menu/tracking.html', {'order': order})

def historial_pedidos(request):
    codes = request.session.get('order_history', [])
    pedidos = Order.objects.filter(tracking_code__in=codes)
    return render(request, 'menu/historial.html', {'pedidos': pedidos})
