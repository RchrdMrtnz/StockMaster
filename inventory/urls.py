from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryHomeView.as_view(), name='inventory-home'),  # Ruta para la vista principal de inventario
    path('productos/', views.ProductoListCreate.as_view(), name='producto-list-create'),
    path('productos/<int:pk>/', views.ProductoDetailUpdateDelete.as_view(), name='producto-detail-update-delete'),
    path('categorias/', views.CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('proveedores/', views.ProveedorListCreate.as_view(), name='proveedor-list-create'),
    path('productos/<int:pk>/', views.ProductoDetalleView.as_view(), name='producto-detalle'),
]
