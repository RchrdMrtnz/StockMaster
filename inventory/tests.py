from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Categoria, Producto, DetalleProducto, Proveedor, StockMovement
from django.urls import reverse

class InventoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.categoria = Categoria.objects.create(nombre='Electronics')
        self.producto = Producto.objects.create(
            nombre='Laptop',
            sku='LPT001',
            categoria=self.categoria,
            cantidad=10,
            min_stock=5
        )
        self.detalle = DetalleProducto.objects.create(
            producto=self.producto,
            precio=1000.00
        )

    def test_kpis_api(self):
        url = reverse('kpis')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_productos'], 1)
        self.assertEqual(response.data['productos_sin_stock'], 0)
        self.assertEqual(response.data['productos_bajo_stock'], 0)

        # Update product to be low stock
        self.producto.cantidad = 3
        self.producto.save()

        response = self.client.get(url)
        self.assertEqual(response.data['productos_bajo_stock'], 1)

    def test_agregar_stock(self):
        url = reverse('agregar-stock', kwargs={'product_id': self.producto.id})
        data = {'cantidad': 5}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 15)

        # Check movement
        movement = StockMovement.objects.last()
        self.assertEqual(movement.producto, self.producto)
        self.assertEqual(movement.cantidad, 5)
        self.assertEqual(movement.tipo_movimiento, 'ENTRADA')

    def test_descontar_stock(self):
        url = reverse('descontar-stock', kwargs={'product_id': self.producto.id})
        data = {'cantidad': 2}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 8)

        # Check movement
        movement = StockMovement.objects.last()
        self.assertEqual(movement.producto, self.producto)
        self.assertEqual(movement.cantidad, -2) # stored as negative
        self.assertEqual(movement.tipo_movimiento, 'SALIDA')

    def test_descontar_insufficient_stock(self):
        url = reverse('descontar-stock', kwargs={'product_id': self.producto.id})
        data = {'cantidad': 20}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 10)

    def test_export_csv(self):
        url = reverse('productos-export')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('ID,Nombre,SKU', content)
        self.assertIn('Laptop', content)

    def test_stock_movement_list(self):
        # Create a movement manually
        StockMovement.objects.create(
            producto=self.producto,
            cantidad=10,
            tipo_movimiento='ENTRADA',
            usuario=self.user
        )

        url = reverse('movimientos-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
