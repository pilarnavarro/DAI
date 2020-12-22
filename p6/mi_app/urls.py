from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
  path('', views.index, name='index'),
  path('autores', views.listaAutores, name='autores'),
  path('autores/nuevo', views.nuevoAutor, name='nuevo_autor'),
  path('autores/editar/<str:pk>/', views.editarAutor, name='editar_autor'),
  path('autores/eliminar/<str:pk>/', views.eliminarAutor, name='eliminar_autor'),
  path('libros', views.listaLibros, name='libros'),
  path('libros/nuevo', views.nuevoLibro, name='nuevo_libro'),
  path('libros/editar/<str:pk>/', views.editarLibro, name='editar_libro'),
  path('libros/eliminar/<str:pk>/', views.eliminarLibro, name='eliminar_libro'),
  path('prestamos', views.listaPrestamos, name='prestamos'),
  path('prestamos/nuevo', views.nuevoPrestamo, name='nuevo_prestamo'),
  path('prestamos/editar/<str:pk>/', views.editarPrestamo, name='editar_prestamo'),
  path('prestamos/eliminar/<str:pk>/', views.eliminarPrestamo, name='eliminar_prestamo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

