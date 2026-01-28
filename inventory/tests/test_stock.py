import pytest
from django.urls import reverse
from inventory.models import StockMovement
from inventory.tests.factories import ProductoFactory

@pytest.mark.django_db
class TestStockOperations:
    def test_add_stock(self, auth_client):
        prod = ProductoFactory(cantidad=10)
        url = reverse('agregar-stock', args=[prod.id])
        data = {'cantidad': 5}
        response = auth_client.post(url, data, format='json')

        assert response.status_code == 200
        prod.refresh_from_db()
        assert prod.cantidad == 15

        movement = StockMovement.objects.last()
        assert movement.tipo_movimiento == 'ENTRADA'
        assert movement.cantidad == 5
        assert movement.producto == prod

    def test_remove_stock_success(self, auth_client):
        prod = ProductoFactory(cantidad=10)
        url = reverse('descontar-stock', args=[prod.id])
        data = {'cantidad': 5}
        response = auth_client.post(url, data, format='json')

        assert response.status_code == 200
        prod.refresh_from_db()
        assert prod.cantidad == 5

        movement = StockMovement.objects.last()
        assert movement.tipo_movimiento == 'SALIDA'
        assert movement.cantidad == -5

    def test_remove_stock_insufficient(self, auth_client):
        prod = ProductoFactory(cantidad=2)
        url = reverse('descontar-stock', args=[prod.id])
        data = {'cantidad': 5}
        response = auth_client.post(url, data, format='json')

        assert response.status_code == 400
        prod.refresh_from_db()
        assert prod.cantidad == 2 # Unchanged
