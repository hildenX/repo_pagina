from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
class Pelicula(models.Model):
    nombre_pelicula = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    fecha_estreno = models.DateField()
    sinopsis = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_pelicula


from django.db import models
from django.contrib.auth.models import User

class Pelicula(models.Model):
    nombre_pelicula = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    fecha_estreno = models.DateField()
    sinopsis = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_pelicula

class Comentario(models.Model):
    pelicula = models.ForeignKey(Pelicula, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} sobre {self.pelicula.nombre_pelicula}"
