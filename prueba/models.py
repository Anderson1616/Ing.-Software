from django.db import models

class Camion(models.Model):
    modelo = models.CharField(max_length=50)
    tipoMarca = models.CharField(max_length=50)
    placa = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.modelo}  {self.tipoMarca}  {self.placa}"

class Conductor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}  {self.apellido1}  {self.apellido2}"

class Pedido(models.Model):
    camion = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    cliente = models.CharField(max_length=100)
    conductor = models.CharField(max_length=100)
    ruta = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=[('En Proceso', 'En Proceso'), ('Finalizado', 'Finalizado')])
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.camion} - {self.cliente}"
