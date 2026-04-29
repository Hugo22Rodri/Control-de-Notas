from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from estudiantes.models import Estudiante

class RegistroNotas(models.Model):
    estudiante = models.OneToOneField(Estudiante, on_delete=models.CASCADE)

    def promedio(self):
        notas = self.detallenota_set.all()
        if notas.exists():
            return round(sum(n.valor for n in notas) / notas.count(), 2)
        return 0

    def estado(self):
        return "Aprobado" if self.promedio() >= 60 else "Reprobado"

    def __str__(self):
        return str(self.estudiante)


class DetalleNota(models.Model):
    registro = models.ForeignKey(RegistroNotas, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    valor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.tipo} - {self.valor}"