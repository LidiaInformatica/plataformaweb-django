from django.urls import path
from . import views
from core.views import dashboard_apoderado

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('mensajes/', views.bandeja_mensajes, name='bandeja_mensajes'),
    path('dashboard-directiva/', views.dashboard_directiva, name='dashboard_directiva'),
    path('redireccion/', views.redireccion_post_login, name='redireccion_post_login'),
    path('dashboard/apoderado/', dashboard_apoderado, name='dashboard_apoderado')
]
