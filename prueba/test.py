# prueba/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import Pedido
from django.contrib.auth.models import User
from .models import Camion

from .models import Conductor;



class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.pedido = Pedido.objects.create(
            camion='ABC123',
            modelo='Modelo X',
            material='Material Y',
            cliente='Cliente Z',
            conductor='Conductor W',
            ruta='Ruta V',
            estado='En Proceso',
            fecha_pedido='2023-06-05'
        )

    def test_home_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registro de Camiones')

    def test_agregar_pedido_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('agregar_pedido'), {
            'camion': 'DEF456',
            'modelo': 'Modelo A',
            'material': 'Material B',
            'cliente': 'Cliente C',
            'conductor': 'Conductor D',
            'ruta': 'Ruta E',
            'estado': 'En Proceso'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pedido.objects.filter(camion='DEF456').exists())

    def test_editar_pedido_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('editar_pedido', args=[self.pedido.id]), {
            'camion': 'GHI789',
            'modelo': 'Modelo B',
            'material': 'Material C',
            'cliente': 'Cliente D',
            'conductor': 'Conductor E',
            'ruta': 'Ruta F',
            'estado': 'Finalizado'
        })
        self.assertEqual(response.status_code, 302)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.camion, 'GHI789')

    def test_eliminar_pedido_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('eliminar_pedido', args=[self.pedido.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Pedido.objects.filter(id=self.pedido.id).exists())

        
class CamionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_agregar_camion_valido(self):
        response = self.client.post(reverse('agregar_camion'), {
            'modelo': 'Cascadia',
            'marca': 'Freightliner',
            'placa': 'C1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Camion.objects.filter(placa='C1234').exists())

    def test_agregar_camion_modelo_vacio(self):
        response = self.client.post(reverse('agregar_camion'), {
            'modelo': '',
            'marca': 'Mack',
            'placa': 'C4444'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Camion.objects.filter(placa='C4444').exists())

    def test_agregar_camion_marca_vacio(self):
        response = self.client.post(reverse('agregar_camion'), {
            'modelo': 'Classic',
            'marca': '',
            'placa': 'C3333'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Camion.objects.filter(placa='C3333').exists())

    def test_agregar_camion_placa_vacio(self):
        response = self.client.post(reverse('agregar_camion'), {
            'modelo': 'Classic',
            'marca': 'Freightliner',
            'placa': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Camion.objects.filter(modelo='Classic', marca='Freightliner').exists())

    def test_ver_informacion_camion(self):
        camion = Camion.objects.create(modelo='Classic', marca='Freightliner', placa='C5555')
        response = self.client.get(reverse('ver_camion', args=[camion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Classic')

    def test_actualizar_camion(self):
        camion = Camion.objects.create(modelo='Classic', marca='Freightliner', placa='C5555')
        response = self.client.post(reverse('editar_camion', args=[camion.id]), {
            'modelo': 'Classic',
            'marca': 'Volvo',
            'placa': 'C5555'
        })
        self.assertEqual(response.status_code, 302)
        camion.refresh_from_db()
        self.assertEqual(camion.marca, 'Volvo')

    def test_mensaje_confirmacion_eliminar_camion(self):
        camion = Camion.objects.create(modelo='Classic', marca='Freightliner', placa='C5555')
        response = self.client.get(reverse('eliminar_camion', args=[camion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Está seguro que desea eliminar este camión?')

    def test_eliminar_camion(self):
        camion = Camion.objects.create(modelo='Classic', marca='Freightliner', placa='C5555')
        response = self.client.post(reverse('eliminar_camion', args=[camion.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Camion.objects.filter(id=camion.id).exists())


class ConductorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_agregar_conductor_valido(self):
        response = self.client.post(reverse('agregar_conductor'), {
            'nombre': 'Alexa',
            'primer_apellido': 'Vega',
            'segundo_apellido': 'Rojas'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Conductor.objects.filter(nombre='Alexa').exists())

    def test_agregar_conductor_nombre_vacio(self):
        response = self.client.post(reverse('agregar_conductor'), {
            'nombre': '',
            'primer_apellido': 'Vargas',
            'segundo_apellido': 'Parrales'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Conductor.objects.filter(primer_apellido='Vargas').exists())

    def test_agregar_conductor_primer_apellido_vacio(self):
        response = self.client.post(reverse('agregar_conductor'), {
            'nombre': 'Anderson',
            'primer_apellido': '',
            'segundo_apellido': 'Ortega'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Conductor.objects.filter(nombre='Anderson').exists())

    def test_agregar_conductor_segundo_apellido_vacio(self):
        response = self.client.post(reverse('agregar_conductor'), {
            'nombre': 'Victoria',
            'primer_apellido': 'Campos',
            'segundo_apellido': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo es obligatorio.')
        self.assertFalse(Conductor.objects.filter(nombre='Victoria').exists())

    def test_ver_informacion_conductor(self):
        conductor = Conductor.objects.create(nombre='Victoria', primer_apellido='Campos', segundo_apellido='Gomez')
        response = self.client.get(reverse('ver_conductor', args=[conductor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Victoria')

    def test_actualizar_conductor(self):
        conductor = Conductor.objects.create(nombre='Victoria', primer_apellido='Campos', segundo_apellido='Gomez')
        response = self.client.post(reverse('editar_conductor', args=[conductor.id]), {
            'nombre': 'Sophie',
            'primer_apellido': 'Campos',
            'segundo_apellido': 'Gomez'
        })
        self.assertEqual(response.status_code, 302)
        conductor.refresh_from_db()
        self.assertEqual(conductor.nombre, 'Sophie')

    def test_mensaje_confirmacion_eliminar_conductor(self):
        conductor = Conductor.objects.create(nombre='Victoria', primer_apellido='Campos', segundo_apellido='Gomez')
        response = self.client.get(reverse('eliminar_conductor', args=[conductor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Está seguro que desea eliminar este conductor?')

    def test_eliminar_conductor(self):
        conductor = Conductor.objects.create(nombre='Victoria', primer_apellido='Campos', segundo_apellido='Gomez')
        response = self.client.post(reverse('eliminar_conductor', args=[conductor.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Conductor.objects.filter(id=conductor.id).exists())
