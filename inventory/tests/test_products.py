import pytest
from django.urls import reverse
from inventory.models import Producto, DetalleProducto
from inventory.tests.factories import ProductoFactory, CategoriaFactory

@pytest.mark.django_db
class TestProducts:
    def test_list_products(self, auth_client):
        ProductoFactory.create_batch(3)
        url = reverse('productos-api')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 3

    def test_create_product(self, auth_client):
        cat = CategoriaFactory()
        url = reverse('productos-api')
        data = {
            'nombre': 'New Product',
            'sku': 'SKU-123',
            'categoria': cat.id,
            'cantidad': 10,
            'precio': 99.99,
            'descripcion': 'A cool product'
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == 201
        assert Producto.objects.count() == 1
        assert DetalleProducto.objects.count() == 1
        assert Producto.objects.get().nombre == 'New Product'

    def test_get_product_details(self, auth_client):
        prod = ProductoFactory()
        url = reverse('producto-detalles', args=[prod.id])
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data['nombre'] == prod.nombre
        assert str(response.data['detalle']['precio']) == str(prod.detalle.precio)

    def test_delete_product(self, auth_client):
        prod = ProductoFactory()
        url = reverse('producto-detail-delete', args=[prod.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Producto.objects.count() == 0
