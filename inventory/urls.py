from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryHomeView.as_view(), name='inventory-home'),
    path('productos/', views.InventoryProduct.as_view(), name='producto-list-create'),
    path('api_productos/', views.ProductoListCreate.as_view(), name='producto-list-view'),
    path('productos/<int:pk>/', views.ProductoDetailUpdateDelete.as_view(), name='producto-detail-update-delete'),
    path('categorias/', views.CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('proveedores/', views.InventoryProviders.as_view(), name='proveedor-list-create'),
    path('api_proveedores/', views.ProveedorListCreate.as_view(), name='proveedor-list-view'),
    path('productos/<int:pk>/', views.ProductoDetalleView.as_view(), name='producto-detalle'),
]
