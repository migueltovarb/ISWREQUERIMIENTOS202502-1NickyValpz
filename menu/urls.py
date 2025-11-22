from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_home, name='menu_home'),
    path('category/<int:category_id>/', views.menu_category, name='menu_category'),
    path('product/<int:product_id>/', views.menu_product_detail, name='menu_product_detail'),

    # Bandeja (carrito)
    path('bandeja/', views.bandeja_view, name='bandeja'),
    path('bandeja/agregar/<int:product_id>/', views.agregar_a_bandeja, name='agregar_a_bandeja'),
    path('bandeja/eliminar/<int:product_id>/', views.eliminar_de_bandeja, name='eliminar_de_bandeja'),
    path('bandeja/vaciar/', views.vaciar_bandeja, name='vaciar_bandeja'),

    # Paso final: formulario de datos del cliente + creación del pedido
    path('realizar-pedido/', views.realizar_pedido, name='realizar_pedido'),

    # Tracking del pedido
    path('tracking/<str:tracking_code>/', views.tracking_view, name='tracking_view'),

    # Historial de pedidos
    path('historial/', views.historial_pedidos, name='historial_pedidos'),
]
