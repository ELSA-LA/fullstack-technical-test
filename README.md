Proyecto Animal Shelter (Shelter API)
=================

## Guidelines

------

API para administrar un albergue de animales rescatados, permitiendo gestionar animales (perros y gatos), voluntarios, adoptantes, y las adopciones. Esta API ofrece operaciones CRUD para cada entidad y está protegida mediante autenticación JWT.

## Índice

1. [Descripción](#descripción)
2. [Características](#características)
3. [Requerimientos](#requerimientos)
4. [Instalación](#instalación)
5. [Uso](#uso)
6. [Autenticación](#autenticación)
7. [Documentación de la API](#documentación-de-la-api)
8. [Contribuciones](#contribuciones)
9. [Licencia](#licencia)

## Descripción

La **Shelter API** es una aplicación diseñada para administrar un albergue de animales, permitiendo llevar el control de:
- Animales en el albergue (nombre, raza, edad, tipo, estado de adopción).
- Voluntarios (información personal y estado).
- Adoptantes (información personal y estado).
- Adopciones (registro de adopciones realizadas).

## Características

- Autenticación mediante JSON Web Tokens (JWT).
- Operaciones CRUD completas para las entidades:
  - Animales
  - Voluntarios
  - Adoptantes
  - Adopciones
- Control de acceso mediante autenticación JWT (utilizando la librería **Simple JWT** para Django REST Framework).

## Requerimientos

- Python 3.8+
- Django 4.0+
- Django REST Framework 3.12+
- Simple JWT

## Instalación

### 1. Clonar el repositorio:

```bash
git clone git@github.com:ELSA-LA/fullstack-technical-test.git
cd fullstack-technical-test/
```

### 2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno:

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DB_NAME
```

### 5. Migraciones:

Ejecuta las migraciones para configurar la base de datos:

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional para el admin):

```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

## Uso

### Endpoints principales

- **Adoptantes**: Gestión de las personas que adoptan animales.
  - `GET /api/adoptants/`: Listar todos los adoptantes.
  - `POST /api/adoptants/`: Crear un adoptante.
  - `GET /api/adoptants/{id}/`: Obtener información de un adoptante.
  - `PUT /api/adoptants/{id}/`: Actualizar adoptante.
  - `PATCH /api/adoptants/{id}/`: Actualizar parcialmente un adoptante.
  - `DELETE /api/adoptants/{id}/`: Eliminar adoptante.

- **Animales**: Gestión de los animales rescatados.
  - `GET /api/animals/`: Listar todos los animales.
  - `POST /api/animals/`: Crear un nuevo animal.
  - `GET /api/animals/{id}/`: Obtener información de un animal.
  - `PUT /api/animals/{id}/`: Actualizar un animal.
  - `PATCH /api/animals/{id}/`: Actualizar parcialmente un animal.
  - `DELETE /api/animals/{id}/`: Eliminar un animal.

- **Adopciones**: Gestión de las adopciones.
  - `GET /api/adoptions/`: Listar todas las adopciones.
  - `POST /api/adoptions/`: Registrar una nueva adopción.
  - `GET /api/adoptions/{id}/`: Obtener detalles de una adopción.
  - `PUT /api/adoptions/{id}/`: Actualizar una adopción.
  - `PATCH /api/adoptions/{id}/`: Actualizar parcialmente una adopción.
  - `DELETE /api/adoptions/{id}/`: Eliminar una adopción.

- **Voluntarios**: Gestión de los voluntarios del albergue.
  - `GET /api/volunteers/`: Listar todos los voluntarios.
  - `POST /api/volunteers/`: Crear un voluntario.
  - `GET /api/volunteers/{id}/`: Obtener información de un voluntario.
  - `PUT /api/volunteers/{id}/`: Actualizar voluntario.
  - `PATCH /api/volunteers/{id}/`: Actualizar parcialmente un voluntario.
  - `DELETE /api/volunteers/{id}/`: Eliminar voluntario.

## Autenticación

La API utiliza autenticación basada en JSON Web Tokens (JWT). Para obtener un token de acceso, realiza una solicitud POST a:

```bash
POST /api/token/
```

Con las credenciales correctas, recibirás un `access_token` y un `refresh_token` que podrás usar para autenticarte en los demás endpoints.

Para refrescar el token:

```bash
POST /api/token/refresh/
```

## Documentación de la API

La documentación detallada de la API se puede consultar en `/api/schema/swagger-ui/`  or  cuando el servidor de desarrollo esté en ejecución.