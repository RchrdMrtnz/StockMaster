from rest_framework import serializers
from .models import Categoria, Producto, Proveedor, DetalleProducto, StockMovement

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class DetalleProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    detalle = DetalleProductoSerializer(read_only=True)
    proveedores = serializers.StringRelatedField(many=True)

    class Meta:
        model = Producto
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    usuario_username = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = StockMovement
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'tipo_movimiento', 'fecha', 'usuario', 'usuario_username', 'motivo']
