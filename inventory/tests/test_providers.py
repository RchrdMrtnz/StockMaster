import pytest
from django.urls import reverse
from inventory.models import Proveedor
from inventory.tests.factories import ProveedorFactory

@pytest.mark.django_db
class TestProviders:
    def test_list_providers(self, auth_client):
        ProveedorFactory.create_batch(3)
        url = reverse('proveedores-api')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 3

    def test_delete_provider(self, auth_client):
        prov = ProveedorFactory()
        url = reverse('proveedor-delete', args=[prov.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Proveedor.objects.count() == 0
