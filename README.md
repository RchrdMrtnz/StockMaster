# StockMaster

**StockMaster** es una solución avanzada de gestión de inventarios, diseñada para optimizar y automatizar el control de productos en almacenes y tiendas. Desarrollado utilizando Django como framework backend y PostgreSQL como sistema de gestión de bases de datos, StockMaster ofrece una API RESTful robusta y flexible que facilita la creación, consulta, actualización y eliminación de productos en el inventario.

## Características principales

### Gestión de Productos
StockMaster permite la administración completa de productos, incluyendo la creación de nuevos ítems, la actualización de información existente, y la eliminación de productos obsoletos. Cada producto puede asociarse a una categoría y a múltiples proveedores, proporcionando una visión detallada y estructurada del inventario.

### Control de Stock
La aplicación incluye funcionalidades para añadir o descontar stock, con validaciones automáticas que aseguran la integridad de los datos y la correcta disponibilidad de productos en el sistema.

### Autenticación y Seguridad
StockMaster integra SimpleJWT para la autenticación basada en tokens JWT, garantizando que solo usuarios autenticados puedan acceder a las operaciones críticas del sistema. Además, se emplean permisos granulares que protegen cada endpoint de la API.

### Paginación y Búsqueda
La API está optimizada para manejar grandes volúmenes de datos con paginación eficiente y permite la búsqueda de productos, categorías y proveedores por términos específicos, mejorando la experiencia de usuario.

### Panel de Administración
StockMaster incluye una interfaz administrativa intuitiva y responsiva, donde los usuarios pueden gestionar categorías, proveedores y productos de manera visual y eficiente.

### Indicadores Clave de Rendimiento (KPIs)
La API ofrece endpoints que calculan y devuelven KPIs esenciales, como el valor total del inventario, el número de productos sin stock, y la cantidad total de proveedores, ayudando a los administradores a tomar decisiones informadas.

### Documentación y Soporte
La aplicación utiliza drf-yasg para generar documentación interactiva de la API, permitiendo a los desarrolladores explorar y probar los endpoints de manera sencilla.

## Tecnologías Utilizadas

- **Django:** Framework web de alto nivel que permite el desarrollo rápido de aplicaciones seguras y mantenibles.
- **Django REST Framework:** Herramienta potente para construir APIs RESTful en Django.
- **PostgreSQL:** Sistema de base de datos relacional utilizado para el almacenamiento seguro y eficiente de datos.
- **JWT (JSON Web Token):** Sistema de autenticación seguro para proteger el acceso a la API.
- **Docker:** (Opcional) Para facilitar el despliegue y la gestión de entornos de desarrollo y producción.

## Guía de Instalación

Sigue los pasos a continuación para instalar y configurar **StockMaster** en tu entorno local.


### 1. Clonar el Repositorio
git clone https://github.com/RchrdMrtnz/StockMaster.git
cd StockMaster

### 2. Instalar `pipenv` y crear el entorno virtual
pip install pipenv
pipenv install
pipenv shell

### 3. Configurar Variables de Entorno
#### Crea un archivo `.env` en la raíz del proyecto para configurar las variables de entorno necesarias. 
#### Asegúrate de incluir las siguientes variables en el archivo `.env`:
```bash
SECRET_KEY='tu-clave-secreta'
DB_NAME='nombre-de-tu-base-de-datos'
DB_USER='tu-usuario-de-base-de-datos'
DB_PASSWORD='tu-contraseña-de-base-de-datos'
DB_HOST='tu-host-de-base-de-datos'
DB_PORT='tu-puerto-de-base-de-datos'
ALLOWED_HOSTS='localhost,127.0.0.1'
CORS_ALLOWED_ORIGINS='http://localhost:3000'
```
### 4. Realizar Migraciones de la Base de Datos
python manage.py migrate

### 5. Crear un Superusuario
python manage.py createsuperuser

### 6. Ejecutar el Servidor de Desarrollo
python manage.py runserver

### Ahora puedes acceder a la aplicación en `http://localhost:8000` y al panel de administración en `http://localhost:8000/admin`.

### 7. Documentación de la API
#### Para explorar y probar los endpoints de la API, visita la documentación interactiva generada por `drf-yasg` en `http://localhost:8000/swagger/`.

## Nota

Asegúrate de tener configurado PostgreSQL y que los valores en tu archivo `.env` correspondan a tu entorno local de base de datos.