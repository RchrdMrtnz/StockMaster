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
            cantidad = request.data.get('cantidad', 0)
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
            cantidad = request.data.get('cantidad', 0)
            if producto.cantidad >= int(cantidad):
                producto.cantidad -= int(cantidad)
                producto.save()
                return Response({'status': 'success', 'message': 'Stock descontado correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Cantidad insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({'status': 'error', 'message': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)


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
