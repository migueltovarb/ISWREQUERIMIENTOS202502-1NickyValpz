from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs del menú público (cliente)
    path('', include('menu.urls')),

    # URLs del sistema de pedidos
    path('orders/', include('orders.urls')),

    # URLs del dashboard interno (admin + barista)
    path('dashboard/', include('dashboard.urls')),
]

# Archivos media (imágenes de productos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
