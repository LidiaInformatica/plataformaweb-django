from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('mensajes/', views.bandeja_mensajes, name='bandeja_mensajes'),
    path('dashboard-directiva/', views.dashboard_directiva, name='dashboard_directiva'),
    path('vista-apoderado/', views.vista_apoderado, name='vista_apoderado'),
    path('redireccion/', views.redireccion_post_login, name='redireccion_post_login')
]
