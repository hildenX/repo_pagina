from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('crud/', views.crud, name='crud'),
    path('logout/', views.custom_logout, name='logout'),
    path('agregar/', views.agregar_pelicula, name='agregar_pelicula'),
    path('pelicula/<int:pelicula_id>/ver/', views.ver_pelicula, name='ver_pelicula'),
    path('pelicula/<int:pelicula_id>/editar/', views.editar_pelicula, name='editar_pelicula'),
    path('pelicula/<int:pelicula_id>/borrar/', views.borrar_pelicula, name='borrar_pelicula'),
    path('ver_pelicula/<int:pelicula_id>/', views.ver_pelicula, name='ver_pelicula'),

]
