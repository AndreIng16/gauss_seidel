from django.contrib import admin
from django.urls import path
from interfaz import views  # Usamos la carpeta interfaz existente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('resolver/', views.resolver, name='resolver'),
    path('resultado/<int:sistema_id>/', views.resultado, name='resultado'),
    path('historial/', views.historial, name='historial'),
    path('eliminar/<int:sistema_id>/', views.eliminar_sistema, name='eliminar_sistema'),
]