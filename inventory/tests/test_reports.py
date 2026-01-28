import pytest
from django.urls import reverse
from inventory.tests.factories import ProductoFactory

@pytest.mark.django_db
class TestReports:
    def test_kpis(self, auth_client):
        ProductoFactory.create_batch(5, cantidad=10)
        url = reverse('kpis')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response.data['total_productos'] == 5

    def test_export_csv(self, auth_client):
        ProductoFactory.create_batch(2)
        url = reverse('productos-export')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert response['Content-Type'] == 'text/csv'
        content = response.content.decode('utf-8')
        assert "Nombre,SKU" in content

    def test_movement_history(self, auth_client):
        url = reverse('movimientos-api')
        response = auth_client.get(url)
        assert response.status_code == 200
