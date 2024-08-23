from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import CreateView

from rest_framework import generics, viewsets, serializers, filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Producto, Categoria, Proveedor, DetalleProducto
from .serializers import ProductoSerializer, CategoriaSerializer, ProveedorSerializer
from django.db.models import Sum, Count, F


#############
# Categoria
#############
class InventoryCategoryView(View):
    template_name = 'inventory/category.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class CategoriaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class CategoriaListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        paginator = CategoriaPagination()
        search_term = request.query_params.get('search', '')

        if search_term:
            categorias = Categoria.objects.filter(nombre__icontains=search_term).order_by('principal__nombre', 'nombre')
        else:
            categorias = Categoria.objects.all().order_by('principal__nombre', 'nombre')

        result_page = paginator.paginate_queryset(categorias, request)
        serializer = CategoriaSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Copiar los datos del request

        # Si el campo principal está vacío, setearlo explícitamente a None
        if not data.get('principal'):
            data['principal'] = None

        serializer = CategoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Categoría creada correctamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetailDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id, *args, **kwargs):
        try:
            categoria = Categoria.objects.get(id=category_id)
            categoria.delete()
            return Response({'status': 'success', 'message': 'Categoría eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Categoria.DoesNotExist:
            return Response({'status': 'error', 'message': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)




#############
# Proveedores
#############


class ProveedorPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100


class CreateProveedorView(CreateView):
    model = Proveedor
    fields = ['nombre', 'informacion_contacto', 'sitio_web', 'correo_electronico', 'telefono']
    success_url = reverse_lazy('proveedor-list-create')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'status': 'success', 'message': 'Proveedor guardado correctamente'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


class ProveedoresAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10

        search_term = request.query_params.get('search', '')

        if search_term:
            proveedores = Proveedor.objects.filter(
                nombre__icontains=search_term
            )
        else:
            proveedores = Proveedor.objects.all()

        result_page = paginator.paginate_queryset(proveedores, request)
        serializer = ProveedorSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def delete(self, request, *args, **kwargs):
        proveedor_id = kwargs.get('pk')
        try:
            proveedor = Proveedor.objects.get(id=proveedor_id)
            proveedor.delete()
            return Response({'status': 'success', 'message': 'Proveedor eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Proveedor.DoesNotExist:
            return Response({'status': 'error', 'message': 'Proveedor no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class InventoryProviders(View):
    template_name = 'inventory/providers.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


#############
# Productos
#############

class ProductoListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 10  
        
        search_term = request.query_params.get('search', '')

        if search_term:
            productos = Producto.objects.filter(
                nombre__icontains=search_term
            )
        else:
            productos = Producto.objects.all()

        result_page = paginator.paginate_queryset(productos, request)
        serializer = ProductoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        producto = Producto.objects.create(
            nombre=data['nombre'],
            sku=data['sku'],
            categoria_id=data['categoria'],
            cantidad=data['cantidad']
        )

        proveedores = data.getlist('proveedores')
        if proveedores:
            producto.proveedores.set(proveedores)

        DetalleProducto.objects.create(
            producto=producto,
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            peso=data.get('peso', None),
            longitud=data.get('longitud', None),
            anchura=data.get('anchura', None),
            altura=data.get('altura', None),
            color=data.get('color', ''),
            material=data.get('material', ''),
            garantia=data.get('garantia', ''),
            otras_especificaciones=data.get('otras_especificaciones', '')
        )

        return Response({'status': 'success', 'message': 'Producto creado correctamente'}, status=status.HTTP_201_CREATED)

class AgregarStockAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            producto = Producto.objects.get(id=product_id)
            cantidad = request.data.get('cantidad')

            # Validación de cantidad
            if not cantidad or not str(cantidad).isdigit() or int(cantidad) <= 0:
                return Response({'status': 'error', 'message': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

            # Agregar la cantidad al stock existente
            producto.cantidad += int(cantidad)
            producto.save()
            return Response({'status': 'success', 'message': 'Stock agregado correctamente'}, status=status.HTTP_200_OK)
        
        except Producto.DoesNotExist:
            return Response({'status': 'error', 'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class DescontarStockAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            producto = Producto.objects.get(id=product_id)
            cantidad = request.data.get('cantidad')

            # Validación de cantidad
            if not cantidad or not str(cantidad).isdigit() or int(cantidad) <= 0:
                return Response({'status': 'error', 'message': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

            cantidad = int(cantidad)

            # Verificar que haya suficiente stock para descontar
            if producto.cantidad >= cantidad:
                producto.cantidad -= cantidad
                producto.save()
                return Response({'status': 'success', 'message': 'Stock descontado correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Cantidad insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Producto.DoesNotExist:
            return Response({'status': 'error', 'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
class ProductoDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        try:
            producto = Producto.objects.get(id=product_id)
            detalle_producto = producto.detalle

            data = {
                "nombre": producto.nombre,
                "sku": producto.sku,
                "categoria": producto.categoria.nombre,
                "cantidad": producto.cantidad,
                "proveedores": [proveedor.nombre for proveedor in producto.proveedores.all()],
                "creado_en": producto.creado_en,
                "actualizado_en": producto.actualizado_en,
                "detalle": {
                    "descripcion": detalle_producto.descripcion,
                    "precio": detalle_producto.precio,
                    "peso": detalle_producto.peso,
                    "longitud": detalle_producto.longitud,
                    "anchura": detalle_producto.anchura,
                    "altura": detalle_producto.altura,
                    "color": detalle_producto.color,
                    "material": detalle_producto.material,
                    "garantia": detalle_producto.garantia,
                    "otras_especificaciones": detalle_producto.otras_especificaciones,
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class ProductoDetailDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            producto = Producto.objects.get(id=product_id)
            producto.delete()
            return Response({'status': 'success', 'message': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({'status': 'error', 'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class InventoryProduct(View):
    template_name = 'inventory/product.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        categorias = Categoria.objects.all()
        proveedores = Proveedor.objects.all()
        context = {
            'categorias': categorias,
            'proveedores': proveedores,
        }
        return render(request, self.template_name, context)


#############
# Vistas generales
#############

class KPIsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_productos = Producto.objects.count()
        valor_total_inventario = Producto.objects.aggregate(valor_total=Sum(F('detalle__precio') * F('cantidad')))['valor_total'] or 0
        productos_sin_stock = Producto.objects.filter(cantidad=0).count()
        total_proveedores = Proveedor.objects.count()

        data = {
            'total_productos': total_productos,
            'valor_total_inventario': valor_total_inventario,
            'productos_sin_stock': productos_sin_stock,
            'total_proveedores': total_proveedores,
        }

        return Response(data, status=200)
    
    
class InventoryHomeView(View):
    template_name = 'inventory/home.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(login_required)  
    def get(self, request, *args, **kwargs):
        context = {
            'welcome_message': 'Bienvenido a StockMaster',
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass
