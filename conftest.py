import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory(db, django_user_model):
    def create_user(**kwargs):
        username = kwargs.pop('username', 'testuser')
        password = kwargs.pop('password', 'password123')
        email = kwargs.pop('email', 'test@example.com')
        # Ensure unique username if called multiple times without args
        if django_user_model.objects.filter(username=username).exists():
            import uuid
            username = f"{username}_{uuid.uuid4().hex[:6]}"

        return django_user_model.objects.create_user(username=username, password=password, email=email, **kwargs)
    return create_user

@pytest.fixture
def auth_client(api_client, user_factory):
    user = user_factory()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.user = user
    return api_client
