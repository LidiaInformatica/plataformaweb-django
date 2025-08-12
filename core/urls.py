from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('mensajes/', views.bandeja_mensajes, name='bandeja_mensajes'),
]
