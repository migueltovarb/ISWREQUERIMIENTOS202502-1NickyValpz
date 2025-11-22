from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse


def generar_factura_pdf(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título
    p.setFont("Helvetica-Bold", 20)
    p.drawString(200, 750, "Factura de Pedido")

    # Datos del cliente
    p.setFont("Helvetica", 12)
    y = 710

    p.drawString(50, y, f"Cliente: {order.customer_name} {order.customer_lastname}")
    y -= 20
    p.drawString(50, y, f"Teléfono: {order.customer_phone}")
    y -= 20
    p.drawString(50, y, f"Método de pago: {order.get_payment_method_display()}")
    y -= 20
    p.drawString(50, y, f"Código de seguimiento: {order.tracking_code}")
    y -= 40

    # Encabezado tabla
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Producto")
    p.drawString(300, y, "Cantidad")
    y -= 20

    # Items
    p.setFont("Helvetica", 12)
    for item in order.items.all():
        p.drawString(50, y, item.product.name)
        p.drawString(300, y, str(item.quantity))
        y -= 20

        if y < 50:  # Nueva página si se llena
            p.showPage()
            y = 750

    # Total
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total: ${order.total}")

    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"Factura_{order.id}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
