# Frontend unificado C2C-UD por roles

Este frontend fue reorganizado para exponer los microservicios desde casos reales de uso, no solamente desde una lista técnica de endpoints.

## Cómo ejecutarlo

```bash
docker compose up --build
```

Luego abre:

- Frontend unificado: `http://localhost:8080`
- Vista usuario: `http://localhost:8080/usuario.html`
- Vista administrador: `http://localhost:8080/admin.html`
- Bandeja Mailpit: `http://localhost:8025`

## Servicios integrados

| Servicio | Puerto host | Proxy desde frontend | Uso principal |
|---|---:|---|---|
| coupon | 8001 | `/api/coupon` | Cupones públicos, asignados, cumpleaños, referidos y aplicación de descuentos |
| email | 8002 | `/api/email` | Envío de plantillas transaccionales y promocionales |
| geolocation | 8003 | `/api/geolocation` | Sedes, puntos, mapa visual y diagrama de ruta |
| report | 8004 | `/api/report` | Radicación, seguimiento, filtros, actualización, eliminación lógica y reintento |

## Vista usuario

Archivo: `frontend/usuario.html`

Permite simular un usuario final del marketplace:

1. Guardar sesión de prueba con nombre, correo e ID.
2. Radicar reportes usando `POST /api/v1/reports/`.
3. Consultar seguimiento con `GET /api/v1/reports/tracking/{radicado}`.
4. Ver sedes cargadas desde `GET /api/v1/geolocation/all_address` en un mapa visual.
5. Buscar una sede por nombre usando `GET /api/v1/geolocation/name/{name}`.
6. Consultar cupones del usuario con `GET /api/v1/users/{email}/coupons`.
7. Aplicar cupones asignados o públicos con los endpoints `apply-assigned` y `apply-unassigned`.

## Vista administrador

Archivo: `frontend/admin.html`

Permite sustentar la lógica del backend por servicio:

### Reportes

- Crear caso demo.
- Listar y filtrar reportes.
- Ver conteo y gráfico por estado técnico de envío.
- Actualizar estado funcional del reporte.
- Reintentar envío cuando el reporte esté pendiente o fallido.
- Eliminar reporte de forma lógica.

### Geolocalización

- Listar sedes y puntos.
- Crear un nuevo punto geográfico.
- Eliminar por ID.
- Mostrar el mapa administrativo.
- Mostrar un diagrama de flujo entre usuario, sede y servicio.

### Cupones

- Crear cupón público/no asignado.
- Crear cupón asignado a usuario.
- Crear cupón de cumpleaños.
- Crear cupón de referido.
- Listar cupones.
- Habilitar, deshabilitar, eliminar y validar estado.
- Consultar usuarios con cupones.

### Correos

- Enviar plantillas con `X-API-Key`.
- API Key local por defecto: `dev-api-key`.
- SMTP local configurado contra Mailpit.
- Ver correos enviados en `http://localhost:8025`.

## Ajustes técnicos incluidos

- Se agregó servicio `frontend` en `docker-compose.yml` usando Nginx.
- Se agregó `frontend/nginx.conf` para servir páginas y proxyear los microservicios.
- Se habilitó CORS en `coupon` y `email`.
- Se configuró el servicio `email` para funcionar con Mailpit sin autenticación SMTP en desarrollo.
- Se agregó configuración local de `report` para Postgres y Mailpit.
- Se corrigió el módulo de cupones para permitir crear, serializar, asignar y aplicar cupones desde formularios reales.

## Validaciones realizadas en este entorno

- `frontend/app.js`: validado con `node --check`.
- `services/coupon`: `85 passed`.
- `services/geolocation`: `51 passed`.
- `services/email`: `24 passed`.
- `services/report`: no se ejecutó en este entorno porque no está instalada la dependencia `sqlalchemy` fuera del contenedor. En Docker se instala desde `services/report/requirements.txt`.
- No se pudo ejecutar `docker compose up --build` aquí porque este entorno no tiene Docker disponible.

## Actualización mapa Leaflet

Se corrigió la visualización del mapa de geolocalización para evitar que OpenStreetMap aparezca cortado o con espacios en blanco dentro de la tarjeta. Los ajustes aplicados fueron:

- Contenedor con altura estable y responsive: `clamp(420px, 58vh, 560px)`.
- `align-items:start` en el grid para que el mapa no se estire por la altura del panel lateral.
- `invalidateSize()` después de crear el mapa, después de cargar marcadores y después de centrar resultados.
- Eliminación del pseudo-fondo del mapa cuando Leaflet está activo.
- Marcadores personalizados con estética UD.
- Mantenimiento del mapa alternativo si Leaflet/OpenStreetMap no carga.
