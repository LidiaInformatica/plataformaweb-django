from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('crear-perfil/', views.crear_perfil_view, name='crear_perfil'),
    path('cambiar-password/', views.cambiar_password_view, name='cambiar_password'),
]
