from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryHomeView.as_view(), name='inventory-home'),
    path('productos/', views.InventoryProduct.as_view(), name='producto-list-create'),
    path('proveedores/', views.InventoryProviders.as_view(), name='proveedor-list-create'),
    path('api/proveedores/', views.ProveedoresAPIView.as_view(), name='proveedores-api'),
    path('proveedores/create/', views.CreateProveedorView.as_view(), name='proveedor-create'),

]
