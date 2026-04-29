from django.db import models

class Estudiante(models.Model):
    id_estudiante = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"