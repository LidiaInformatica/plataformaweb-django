# core/notificacion_urls.py
from django.urls import path
from . import notificacion_views
from core.views_notificaciones import enviar_notificacion_manual


app_name = 'notificaciones'

urlpatterns = [
    path('', notificacion_views.lista_notificaciones, name='lista'),
    path('<int:notificacion_id>/', notificacion_views.detalle_notificacion, name='detalle'),
    path('<int:notificacion_id>/marcar_leida/', notificacion_views.marcar_leida, name='marcar_leida'),
    path('test/', notificacion_views.test_notificacion, name='test'),
    path('enviar/', enviar_notificacion_manual, name='enviar_notificacion_manual'),
]
