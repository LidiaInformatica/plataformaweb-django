from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard principal y redirección
    path('', views.dashboard, name='dashboard'),
    path('redireccion/', views.redireccion_post_login, name='redireccion_post_login'),
    
    # Dashboards específicos
    path('dashboard/apoderado/', views.dashboard_apoderado, name='dashboard_apoderado'),
    path('dashboard/directiva/', views.dashboard_directiva, name='dashboard_directiva'),
    
    # Mensajes y notificaciones
    path('mensajes/', views.bandeja_mensajes, name='bandeja_mensajes'),
    
    # Errores
    path('error/apoderado/', views.error_apoderado, name='error_apoderado'),
]