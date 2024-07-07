from django.db import models
from django.core.exceptions import ValidationError
class Libro(models.Model):
    id= models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, verbose_name="Titulo")
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    descripcion = models.TextField(null=True, verbose_name="Descripcion")
    error_messages = {
            'titulo': {
                'required': 'El campo Titulo no puede estar vacío.',
            },
            'descripcion': {
                'required': 'El campo Descripción no puede estar vacío.',
            },
            'imagen': {
                'invalid_image': "Solo se permiten archivos con formato PNG, JPG, o JPEG.",
            },
        }
    def __str__(self):
        fila = "Titulo: " + self.titulo + " - " +"Descripcion: " + self.descripcion
        return fila
    

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
   
    def save(self, *args, **kwargs):
        try:
            old_instance = Libro.objects.get(id=self.id)
            if old_instance.imagen != self.imagen:
                old_instance.imagen.delete(save=False)
        except Libro.DoesNotExist:
            pass
        super().save(*args, **kwargs)