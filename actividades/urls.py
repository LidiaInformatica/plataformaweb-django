from django.urls import path
from . import views

app_name = 'actividades'

urlpatterns = [
    path('', views.lista_actividades, name='lista'),
    path('crear/', views.crear_actividad, name='crear'),
    path('<int:pk>/', views.ver_actividad, name='ver'),
    path('<int:pk>/editar/', views.editar_actividad, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar_actividad, name='eliminar'),
    path('exportar/', views.exportar_actividades, name='exportar'),
]
