from django.db import models

TEXT_KEYS = (('sitename','Nombre del Sitio'),)
NUM_KEYS = (('extrapicprice', 'Precio por foto extra'),)


# Create your models here.
class TextVars(models.Model):
    key = models.CharField(max_length=30, unique=True, choices=TEXT_KEYS)
    value = models.TextField()

class NumVars(models.Model):
    key = models.CharField(max_length=30, unique=True, choices=NUM_KEYS)
    value = models.DecimalField(max_digits=12, decimal_places=2)

