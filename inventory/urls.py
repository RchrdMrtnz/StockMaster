from django.urls import path
from . import views

urlpatterns = [
    path('', views.InventoryHomeView.as_view(), name='inventory-home'),
    path('productos/', views.InventoryProduct.as_view(), name='producto-list-create'),
    
    # API de Productos
    path('api/productos/', views.ProductoListCreateAPIView.as_view(), name='productos-api'),
    path('api/productos/<int:product_id>/agregar_stock/', views.AgregarStockAPIView.as_view(), name='agregar-stock'),
    path('api/productos/<int:product_id>/descontar_stock/', views.DescontarStockAPIView.as_view(), name='descontar-stock'),
    path('api/productos/<int:product_id>/delete/', views.ProductoDetailDeleteAPIView.as_view(), name='producto-detail-delete'),
    path('api/productos/<int:product_id>/detalles/', views.ProductoDetailAPIView.as_view(), name='producto-detalles'),

    # Proveedores
    path('proveedores/', views.InventoryProviders.as_view(), name='proveedor-list-create'),
    path('api/proveedores/', views.ProveedoresAPIView.as_view(), name='proveedores-api'),
    path('proveedores/create/', views.CreateProveedorView.as_view(), name='proveedor-create'),
    path('api/proveedores/<int:pk>/', views.ProveedoresAPIView.as_view(), name='proveedor-delete'),
    
    # categoria 
    path('api/categorias/', views.CategoriaListCreateAPIView.as_view(), name='categoria-list-create'),
    path('api/categorias/<int:category_id>/', views.CategoriaDetailDeleteAPIView.as_view(), name='categoria-delete'),
    path('categorias/', views.InventoryCategoryView.as_view(), name='categoria-list'),

    #kpis
    path('api/kpis/', views.KPIsAPIView.as_view(), name='kpis'),
    
    
]
