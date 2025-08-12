# core/notificacion_urls.py
from django.urls import path
from . import notificacion_views

app_name = 'notificaciones'

urlpatterns = [
    path('', notificacion_views.lista_notificaciones, name='lista'),
    path('<int:notificacion_id>/', notificacion_views.detalle_notificacion, name='detalle'),
    path('<int:notificacion_id>/marcar_leida/', notificacion_views.marcar_leida, name='marcar_leida'),
    path('test/', notificacion_views.test_notificacion, name='test'),
]
