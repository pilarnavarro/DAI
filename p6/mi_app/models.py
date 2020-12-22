from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator

class Autor(models.Model):
	nombre=models.CharField(max_length=100) 
	nacimiento=models.DateField("fecha de nacimiento", blank=True, null=True)

	def __str__(self):
		return self.nombre


	class Meta:
		verbose_name_plural = "autores"

class Libro(models.Model):
	codigo=models.IntegerField(primary_key=True,validators=[MaxValueValidator(50000), MinValueValidator(0)])
	titulo=models.CharField(max_length=200) 
	publicacion=models.DateField("fecha de publicacion", blank=True, null=True)
	portada=models.ImageField(upload_to='images/', blank=True,null=True)
	resumen=models.TextField(blank=True,max_length=500,null=True)
	autor=models.ManyToManyField(Autor)

	def __str__(self):
		autores=""
		for x in self.autor.all():
			autores=autores + '{}, '.format(x)
		autores = autores[:-2]
		return self.titulo + ' ({})'.format(autores)

class Prestamo(models.Model):
	libro=models.ForeignKey(Libro, on_delete=models.CASCADE)
	fecha=models.DateTimeField("fecha prestamo", default=timezone.now)
	usuario=models.CharField(max_length=100)

	def __str__(self):
		return '{}'.format(self.libro) + ' prestado a ' + self.usuario