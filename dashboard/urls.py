from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home
    path('', views.dashboard_home, name='dashboard_home'),

    # Productos
    path('productos/', views.product_list, name='product_list'),
    path('productos/crear/', views.product_create, name='product_create'),
    path('productos/editar/<int:product_id>/', views.product_edit, name='product_edit'),
    path('productos/eliminar/<int:product_id>/', views.product_delete, name='product_delete'),

    # Categorías
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/crear/', views.category_create, name='category_create'),
    path('categorias/editar/<int:category_id>/', views.category_edit, name='category_edit'),
    path('categorias/eliminar/<int:category_id>/', views.category_delete, name='category_delete'),

    # Baristas
    path('baristas/', views.barista_list, name='barista_list'),
    path('baristas/crear/', views.barista_create, name='barista_create'),
    path('baristas/editar/<int:user_id>/', views.barista_edit, name='barista_edit'),
    path('baristas/eliminar/<int:user_id>/', views.barista_delete, name='barista_delete'),

    # Pedidos
    path('pedidos/', views.pedidos_list, name='pedidos_list'),
    path('pedidos/<int:order_id>/', views.pedido_detalle, name='pedido_detalle'),
    path('pedidos/estado/<int:order_id>/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]
