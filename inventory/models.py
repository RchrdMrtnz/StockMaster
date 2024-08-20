from django.db import models

# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    principal = models.ForeignKey('self', null=True, blank=True, related_name='secundarias', on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = ('nombre', 'principal')
        verbose_name_plural = "categorías"
        db_table = 'categoria'

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)  # Código de producto único
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    proveedores = models.ManyToManyField('Proveedor', related_name='productos')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'

class DetalleProducto(models.Model):
    producto = models.OneToOneField(Producto, related_name='detalle', on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=20, decimal_places=2)  # Campo obligatorio
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    anchura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    altura = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    garantia = models.CharField(max_length=100, blank=True)
    otras_especificaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Detalles de {self.producto.nombre}"

    class Meta:
        db_table = 'detalle_producto'

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    informacion_contacto = models.TextField(blank=True)
    sitio_web = models.URLField(blank=True)
    correo_electronico = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'proveedor'




