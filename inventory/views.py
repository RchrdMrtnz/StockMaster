from rest_framework import generics
from .models import Producto, Categoria, Proveedor
from .serializers import ProductoSerializer, CategoriaSerializer, ProveedorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views import View
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class ProductoListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ProductoDetailUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CategoriaListCreate(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ProveedorListCreate(generics.ListCreateAPIView):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
class ProductoDetalleView(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



class InventoryHomeView(View):
    template_name = 'inventory/home.html'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(login_required)  # Asegura que solo usuarios autenticados puedan acceder
    def get(self, request, *args, **kwargs):
        context = {
            'welcome_message': 'Bienvenido a StockMaster',
            # Aquí puedes agregar más contexto o lógica para la vista
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        # Aquí puedes manejar la lógica de un formulario o cualquier acción de post
        pass
    

class InventoryProduct(View):
    template_name = 'inventory/product.html'
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


class InventoryProviders(View):
    template_name = 'inventory/providers.html'
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
