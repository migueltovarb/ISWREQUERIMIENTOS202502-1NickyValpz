from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_pedido, name='crear_pedido'),

    # Tracking corregido
    path('tracking/<str:tracking_code>/', views.tracking, name='tracking'),
]
