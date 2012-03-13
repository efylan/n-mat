from django.db import models
from django.contrib import admin

class Estado(models.Model):
    nombre = models.CharField(max_length=40)
    def __unicode__(self):
        return self.nombre

try:
    admin.site.register(Estado)
except:
    pass

class Municipio(models.Model):
    estado = models.ForeignKey(Estado)
    nombre = models.CharField(max_length=70)
    def __unicode__(self):
        return self.nombre

try:
    admin.site.register(Municipio)
except:
    pass

