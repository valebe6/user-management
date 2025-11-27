# Users CRUD API — Flask + MongoDB + Docker + Swagger

API REST sencilla para manejo de usuarios (CRUD) usando Flask y MongoDB. Incluye validación de datos, paginación básica, manejo de errores y documentación con Swagger UI.

---

## Tecnologías usadas

- **Python 3**
- **Flask**
- **MongoDB**
- **Docker + Docker Compose**
- **PyMongo**
- **Marshmallow**
- **Flasgger (Swagger)**

---

## Funcionalidades

- Crear usuario
- Listar usuarios con paginación
- Obtener usuario por ID
- Actualizar usuario por ID (PUT/PATCH)
- Eliminar usuario por ID
- Email único (índice `unique`)
- Documentación interactiva con Swagger

---

## Requisitos

- Python 3.10+
- Docker y Docker Compose

---

## Instalación y ejecución (modo local)

### 1) Clonar y entrar al proyecto

```
git clone https://github.com/valebe6/user-management.git
cd users-api
```

### 2) Crear y activar entorno virtual

Linux/WSL/Mac

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```
python -m venv .venv
.venv\Scripts\activate
```

### 3) Instalar dependencias

```
pip install -r requirements.txt
```

### 4) Levantar MongoDB con Docker

```
docker compose up -d
```

Verifica:

```
docker ps
```

### 5) Ejecutar la API

```
python run.py
```

La API corre en:

- API Base URL: http://127.0.0.1:5000/api/users
- Swagger UI: http://127.0.0.1:5000/apidocs/

## Ejecutar todo con Docker (API + Mongo)

### 1) Construir y levantar servicios

```
docker compose up --build
```

La API queda expuesta en:
http://localhost:5000/api/users

## Endpoints

### Crear usuario

POST /api/users

Body ejemplo:

```
{
  "name": "Valentina",
  "email": "val@gmail.com",
  "age": 25
}
```

Respuesta:

- 201 Created
- 409 Conflict si email ya existe
- 400 Bad Request si validación falla

### Listar usuarios (paginado)

GET /api/users?page=1&limit=10

Respuesta:

```
{
  "page": 1,
  "limit": 10,
  "items": [...]
}
```

### Obtener usuario por ID

GET /api/users/{id}

- 200 OK
- 404 Not Found
- 400 Bad Request si ID inválido

### Actualizar usuario por ID

PATCH /api/users/{id}

Body ejemplo:

```
{
  "age": 26
}
```

- 200 OK
- 404 Not Found
- 409 Conflict si email duplicado
- 400 Bad Request validación inválida

### Eliminar usuario por ID

DELETE /api/users/{id}

- 204 No Content
- 404 Not Found
- 400 Bad Request si ID inválido

## Ver datos en Mongo (Docker)

Entrar a Mongo:

```
docker exec -it mongo_users_api mongosh -u root -p root --authenticationDatabase admin
```

Cambiar a la base:

```
use usersdb
```

Ver usuarios:

```
db.users.find().pretty()
```

Salir:

```
exit
```
