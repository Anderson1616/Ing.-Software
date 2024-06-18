# prueba/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import Pedido
from django.contrib.auth.models import User

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
