from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from clasificados.models import ClasifCasa, ClasifAuto
# Create your models here.
STAFF=1
CLIENTE=2

TIPO_CHOICES = ((STAFF,'Staff'),(CLIENTE,'Cliente'))

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    telefono = models.CharField(max_length=30)
    celular = models.CharField(max_length=30)
    direccion = models.TextField()
    tipo = models.PositiveSmallIntegerField(choices=TIPO_CHOICES)
    fav_autos = models.ManyToManyField(ClasifAuto)
    fav_casas = models.ManyToManyField(ClasifCasa)

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','telefono','celular','direccion','tipo')

try:
    admin.site.register(Profile, ProfileAdmin)
except:
    pass



