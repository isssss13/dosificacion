from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class linea(models.Model):
    nombreLinea=models.CharField(max_length=15)
    colorLinea=models.CharField(max_length=15)
    no_estaciones=models.IntegerField(default=0)

class estaciones(models.Model):
    estacion=models.CharField(max_length=50)
    statusSistema=models.BooleanField()
    id_linea=models.ForeignKey(linea, on_delete=models.CASCADE)

class HistoricoAfluencia(models.Model):
    fecha=models.DateTimeField()
    conteo=models.IntegerField(default=0)
    id_estacion=models.ForeignKey(estaciones,on_delete=models.CASCADE)

class Trenes(models.Model):
    fecha=models.DateField()
    conteoTrenes=models.IntegerField(default=0)
    id_estacion=models.ForeignKey(estaciones,on_delete=models.CASCADE)