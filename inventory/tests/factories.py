import factory
from factory.django import DjangoModelFactory
from inventory.models import Categoria, Proveedor, Producto, DetalleProducto

class CategoriaFactory(DjangoModelFactory):
    class Meta:
        model = Categoria

    nombre = factory.Faker('word')
    descripcion = factory.Faker('sentence')

class ProveedorFactory(DjangoModelFactory):
    class Meta:
        model = Proveedor

    nombre = factory.Faker('company')
    correo_electronico = factory.Faker('email')
    telefono = factory.Faker('phone_number')

class DetalleProductoFactory(DjangoModelFactory):
    class Meta:
        model = DetalleProducto

    # We assume 'producto' is passed in when created via RelatedFactory,
    # or we can define a SubFactory but it might cause recursion if not careful.
    # For now, we expect this to be created mostly via ProductoFactory.
    producto = factory.SubFactory('inventory.tests.factories.ProductoFactory')
    precio = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    descripcion = factory.Faker('sentence')

class ProductoFactory(DjangoModelFactory):
    class Meta:
        model = Producto

    nombre = factory.Faker('word')
    sku = factory.Sequence(lambda n: f'SKU-{n}')
    categoria = factory.SubFactory(CategoriaFactory)
    cantidad = factory.Faker('random_int', min=1, max=100)
    min_stock = 5

    # Create the related OneToOne detail automatically
    detalle = factory.RelatedFactory(
        DetalleProductoFactory,
        factory_related_name='producto'
    )
