from django.contrib import admin

# Register your models here.
from .models import linea
from .models import estaciones

admin.site.register(linea)
admin.site.register(estaciones)