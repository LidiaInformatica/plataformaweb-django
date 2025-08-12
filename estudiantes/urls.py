from django.urls import path
from . import views

app_name = 'estudiantes'

urlpatterns = [
    path('', views.lista_estudiantes, name='lista'),
    path('nuevo/', views.crear_estudiante, name='crear'),
    path('<int:pk>/editar/', views.editar_estudiante, name='editar'),
    path('<int:pk>/ver/', views.ver_estudiante, name='ver'),
    path('<int:pk>/eliminar/', views.eliminar_estudiante, name='eliminar'),
    path('ajax/buscar-apoderado/', views.buscar_apoderado_ajax, name='buscar_apoderado_ajax'),
]
