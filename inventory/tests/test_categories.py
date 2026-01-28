import pytest
from django.urls import reverse
from inventory.models import Categoria
from inventory.tests.factories import CategoriaFactory

@pytest.mark.django_db
class TestCategories:
    def test_list_categories(self, auth_client):
        CategoriaFactory.create_batch(3)
        url = reverse('categoria-list-create')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 3

    def test_create_category(self, auth_client):
        url = reverse('categoria-list-create')
        data = {'nombre': 'New Category', 'descripcion': 'Desc'}
        response = auth_client.post(url, data, format='json')
        assert response.status_code == 201
        assert Categoria.objects.count() == 1
        assert Categoria.objects.get().nombre == 'New Category'

    def test_delete_category(self, auth_client):
        cat = CategoriaFactory()
        url = reverse('categoria-delete', args=[cat.id])
        response = auth_client.delete(url)
        assert response.status_code == 204
        assert Categoria.objects.count() == 0
