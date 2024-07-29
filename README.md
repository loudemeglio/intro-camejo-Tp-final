# intro-camejo-Tp-final

# web-
Página tienda - Materia: Introducción al Desarrollo de Software

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install psycopg2-binary
pip install SQLAlchemy Flask-SQLAlchemy
pip install flask-cors
```

## Run

```bash
source venv/bin/activate
cd backend
python3 main.py
```

# FairHome 

Bienvenido a nuestra página web 'FairHome', una tienda en linea de muebles. Este proyecto utiliza en su desarrollo tecnologías como HTML, CSS, JavaScript y Bootstrap para construir el frontend, y Flasc con SQLAlchemy en el backend.
FairHome es una tienda que permite a los usuarios explorar una variedad de muebles, acceder a los productos por su categoría y agregarlos al carrito de compras. Los administradores pueden agregar y eliminar productos desde la interfaz.

### Frontend 

* La página principal de la web incluye una barra de navegación con enlaces a **Home**, **Login** y **Cart**. Además cuena con un dropdown de las categorías disponibles en la web. 

* El carrito de compras se actualiza dinámicamente cuando se van agregando los productos utilizando el botón 'agregar al carrito'. Luego dentro del carrito esta la opción de actualizar la cantidad de cada producto (agregando o sacando) y o eliminar el producto si se desea.

* Dentro del Login se despliega un formulario donde pueden acceder los administradores. Los administradores tienen opciones adicionales como "Agregar Producto" y "Eliminar Producto" de los que se muestran en la página. 

* Los productos se cargan por categorías y así se visualizan en la pagina. 


### Backend

* Para construir el backend se utilizó Flask y SQLAlchemy para manejar las rutas y las operaciones de la base de datos. (Los modelos de las tablas para la base de datos se pueden ver en el archivo models.py dentro del directorio de backend).


### Alumnos
Ignacio Mahmoud Abalos, Lourdes De Meglio y Gaspar Amato
