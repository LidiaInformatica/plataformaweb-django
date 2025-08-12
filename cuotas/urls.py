from django.urls import path
from . import views

app_name = 'cuotas'

urlpatterns = [
    path('', views.lista_pagos, name='lista_pagos'),
    path('registrar/', views.registrar_pago, name='registrar_pago'),
    path('historial/<int:actividad_id>/', views.historial_actividad, name='historial_actividad'),
    path('exportar/', views.exportar_pagos, name='exportar_pagos'),
    path('estado-apoderado/', views.estado_pago_apoderado, name='estado_apoderado'),
]
