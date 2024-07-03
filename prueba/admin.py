# admin.py
from django.contrib import admin
from .models import Conductor, Pedido, Camion

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido1', 'apellido2')

@admin.register(Camion)
class CamionAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'tipoMarca', 'placa')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('camion', 'modelo', 'material', 'cliente', 'conductor', 'ruta', 'estado', 'fecha_pedido')

