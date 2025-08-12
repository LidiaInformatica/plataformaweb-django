"""
URL configuration for plataformaweb project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Added accounts URL
    path('', include('core.urls')),
    path('estudiantes/', include('estudiantes.urls')),
    path('actividades/', include('actividades.urls')),
    path('cuotas/', include('cuotas.urls')),
    path('notificaciones/', include('core.notificacion_urls')),  # Notificaciones URL
]
