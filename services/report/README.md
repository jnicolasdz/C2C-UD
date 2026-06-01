# Backend de Reportes - UD Marketplace

Microservicio básico en **FastAPI** para gestionar reportes dentro de un marketplace universitario.

Incluye:

- CRUD completo de reportes.
- Generación automática de radicado.
- Consulta de seguimiento por radicado.
- Envío de correo de confirmación.
- PostgreSQL con Docker.
- Mailpit para probar correos localmente.
- Documentación automática con Swagger en `/docs`.

---

## 1. Estructura del proyecto

```txt
app/
├── main.py
├── core/
│   ├── config.py
│   └── email.py
├── database/
│   └── connection.py
├── models/
│   └── report_model.py
├── routers/
│   └── report_router.py
├── schemas/
│   └── report_schema.py
├── services/
│   └── report_service.py
└── utils/
    └── radicado.py
```

---

## 2. Levantar el backend con Docker

Desde la carpeta del proyecto:

```bash
docker compose up --build
```

La API quedará disponible en:

```txt
http://localhost:8004
```

Documentación interactiva:

```txt
http://localhost:8004/docs
```

Interfaz para revisar correos enviados localmente:

```txt
http://localhost:8025
```

Base de datos PostgreSQL expuesta localmente en:

```txt
localhost:5434
```

Dentro de Docker, la API se conecta a PostgreSQL usando:

```txt
db:5432
```

---

## 3. Endpoints principales

| Método | Ruta | Función |
|---|---|---|
| GET | `/health` | Verificar que la API está viva |
| POST | `/api/v1/reports` | Crear reporte |
| GET | `/api/v1/reports` | Listar reportes |
| GET | `/api/v1/reports/{id}` | Consultar reporte por ID |
| GET | `/api/v1/reports/tracking/{radicado}` | Consultar reporte por radicado |
| PUT | `/api/v1/reports/{id}` | Actualizar reporte |
| DELETE | `/api/v1/reports/{id}` | Eliminar reporte |

---

## 4. Crear un reporte

Ejemplo de petición:

```json
{
  "user_name": "Sebastián Henriquez",
  "user_email": "usuario@correo.com",
  "report_type": "Problema con publicación",
  "subject": "No aparece mi producto publicado",
  "description": "El producto fue creado, pero no aparece en el marketplace."
}
```

Respuesta esperada:

```json
{
  "id": 1,
  "radicado": "RPT-20260601-ABC12345",
  "user_name": "Sebastián Henriquez",
  "user_email": "usuario@correo.com",
  "report_type": "Problema con publicación",
  "subject": "No aparece mi producto publicado",
  "description": "El producto fue creado, pero no aparece en el marketplace.",
  "status": "RECIBIDO",
  "response_message": null,
  "created_at": "2026-06-01T10:00:00",
  "updated_at": "2026-06-01T10:00:00"
}
```

Cuando el reporte se crea correctamente, el sistema envía un correo con el radicado. En desarrollo puedes ver ese correo en Mailpit:

```txt
http://localhost:8025
```

---

## 5. Estados permitidos

```txt
RECIBIDO
EN_REVISION
EN_PROCESO
RESUELTO
RECHAZADO
CERRADO
```

---

## 6. Dónde modificar cada cosa

| Necesidad | Archivo |
|---|---|
| Cambiar el nombre de la tabla | `app/models/report_model.py` |
| Agregar una columna en base de datos | `app/models/report_model.py` |
| Cambiar campos que recibe el POST | `app/schemas/report_schema.py` |
| Cambiar campos que devuelve la API | `app/schemas/report_schema.py` |
| Cambiar lógica de creación, actualización o eliminación | `app/services/report_service.py` |
| Cambiar rutas de la API | `app/routers/report_router.py` |
| Cambiar conexión a base de datos | `.env` |
| Cambiar configuración SMTP/correo | `.env` y `app/core/email.py` |
| Cambiar formato del radicado | `app/utils/radicado.py` |
| Cambiar puerto | `Dockerfile` y `docker-compose.yml` |

---

## 7. Nota sobre cambios en tablas

Este proyecto crea las tablas automáticamente al iniciar con:

```python
Base.metadata.create_all(bind=engine)
```

Eso sirve para pruebas académicas y desarrollo inicial. Para producción o cambios fuertes de base de datos, lo recomendado es usar migraciones con Alembic.

---

## 8. Probar sin frontend

Puedes probar todo desde Swagger:

```txt
http://localhost:8004/docs
```

También puedes usar el archivo:

```txt
requests.http
```

con la extensión REST Client de VS Code.
