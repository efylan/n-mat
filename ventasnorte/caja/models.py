from django.db import models
from clasificados.models import ClasifCasa, ClasifAuto, Paquete
# Create your models here.
TIPO_CHOICES = ((1,'Auto'), (2,'Casa'))

class Venta(models.Model):
    paquete=models.ForeignKey(Paquete)
    nombre_paquete = models.CharField(max_length=30)    

    precio_paquete = models.DecimalField(max_digits=10, decimal_places=2)
    precio_prioridad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_foto = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Precio de foto extra")
    precio_texto = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Precio de texto extra")

    fotos_extra = models.IntegerField()
    texto_extra = models.BooleanField()
    prioridad = models.BooleanField()

    min_texto = models.IntegerField()
    min_fotos = models.IntegerField()

    total = models.DecimalField(max_digits=9, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    tipo = models.PositiveSmallIntegerField()
    auto = models.ForeignKey(ClasifAuto, blank=True, null=True)
    casa = models.ForeignKey(ClasifCasa, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.nombre_paquete)

    def get_importe_foto(self):
        importe = self.fotos_extra * self.precio_foto
        return importe

    def get_clasificado(self):
        if self.tipo == 1:
            return self.auto
        else:
            return self.casa
