# Frontend C2C-UD por roles

Frontend unificado para exponer y probar los cuatro microservicios del proyecto C2C-UD:

- `coupon`: cupones y descuentos.
- `email`: envío de correos transaccionales y promocionales.
- `geolocation`: sedes/puntos geográficos de Bogotá.
- `report`: radicación, seguimiento y administración de reportes.

La interfaz mantiene una estética institucional basada en rojo, blanco, tarjetas limpias y flujos por rol.

---

## 1. Ejecución

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Luego abrir:

- Inicio: `http://localhost:8080`
- Vista usuario: `http://localhost:8080/usuario.html`
- Vista administrador: `http://localhost:8080/admin.html`
- Bandeja de correos Mailpit: `http://localhost:8025`

El frontend se publica con Nginx y consume los servicios por proxy:

| Ruta frontend | Servicio interno | Puerto local directo |
|---|---|---|
| `/api/coupon` | `coupon:8000/api/v1` | `localhost:8001/api/v1` |
| `/api/email` | `email:8000/api/v1` | `localhost:8002/api/v1` |
| `/api/geolocation` | `geolocation:8000/api/v1` | `localhost:8003/api/v1` |
| `/api/report` | `report:8000/api/v1` | `localhost:8004/api/v1` |

---

## 2. Estructura del frontend

```text
frontend/
├── index.html        # Entrada principal y verificación de servicios
├── usuario.html      # Casos de uso de usuario final
├── admin.html        # Panel de administración y pruebas técnicas
├── app.js            # Consumo de endpoints, renderizado y lógica de casos demo
├── styles.css        # Estética UD y responsive design
├── nginx.conf        # Proxy de servicios para evitar problemas CORS en demo
└── README.md         # Esta guía
```

---

## 3. Vista usuario

`usuario.html` está pensada para una persona que interactúa con la plataforma sin privilegios administrativos.

### 3.1 Reportes

Permite radicar un reporte desde un formulario real con datos de usuario, tipo, asunto y descripción.

Endpoint usado:

```http
POST /api/report/reports/
```

También permite consultar el seguimiento por radicado:

```http
GET /api/report/reports/tracking/{radicado}
```

Caso sugerido para exposición:

1. Guardar datos del usuario.
2. Presionar “Cargar caso de prueba”.
3. Enviar el reporte.
4. Copiar el radicado generado.
5. Consultarlo en el bloque de seguimiento.

### 3.2 Geolocalización

Muestra un mapa real de Bogotá usando Leaflet y OpenStreetMap. El mapa usa exactamente las coordenadas `latitude` y `longitude` que retorna el microservicio.

Endpoints usados:

```http
GET /api/geolocation/geolocation/all_address
GET /api/geolocation/geolocation/id/{location_id}
GET /api/geolocation/geolocation/name/{name}
GET /api/geolocation/geolocation/address/{address}
```

Casos sugeridos:

1. Cargar todas las sedes con “Actualizar mapa”.
2. Buscar por ID `5` para centrar la Sede Tecnológica.
3. Buscar por nombre exacto `Sede Paiba`.
4. Buscar por dirección exacta `Cra 7 #40-62, Bogotá, Colombia`.
5. Dar clic sobre un marcador para ver la información de la sede.

El mapa fue corregido para evitar renderizados incompletos: tiene altura fija responsive, `invalidateSize()` después de cargar marcadores, contenedor sin pseudo-elementos superpuestos y marcadores personalizados UD.

### 3.3 Cupones

Permite consultar cupones asociados al usuario y aplicar un descuento sobre un precio.

Endpoints usados:

```http
GET /api/coupon/users/{email}/coupons
POST /api/coupon/users/{email}/coupons/{coupon_code}/apply-assigned?original_price={precio}
POST /api/coupon/users/{email}/coupons/{coupon_code}/apply-unassigned?original_price={precio}
```

Caso sugerido:

1. Entrar primero a `admin.html`.
2. Crear cupones demo.
3. Volver a `usuario.html`.
4. Consultar cupones.
5. Aplicar un cupón asignado o público.

---

## 4. Vista administrador

`admin.html` concentra gestión, revisión y pruebas de endpoints.

### 4.1 Reportes

Permite crear reportes demo, listar, filtrar, actualizar estado, reintentar notificación y eliminar lógicamente.

Endpoints usados:

```http
POST /api/report/reports/
GET /api/report/reports/
GET /api/report/reports/pending
GET /api/report/reports/failed
GET /api/report/reports/tracking/{radicado}
GET /api/report/reports/{report_id}
PUT /api/report/reports/{report_id}
POST /api/report/reports/{report_id}/retry
DELETE /api/report/reports/{report_id}
```

La vista incluye:

- Tarjetas de conteo.
- Tabla de reportes.
- Gráfica simple por estado de envío.
- Botones de acción por fila.
- Formulario de actualización de estado.

### 4.2 Geolocalización

Permite administrar sedes y puntos de Bogotá.

Endpoints usados:

```http
GET /api/geolocation/geolocation/all_address
GET /api/geolocation/geolocation/id/{location_id}
GET /api/geolocation/geolocation/name/{name}
GET /api/geolocation/geolocation/address/{address}
POST /api/geolocation/geolocation/add/{name}/{description}/{address}/{latitude}/{longitude}
DELETE /api/geolocation/geolocation/{location_id}
```

Casos sugeridos:

1. Clic en `GET /geolocation/all_address` para cargar sedes.
2. Buscar por ID `5` y verificar que el mapa se centre en el marcador.
3. Crear un punto de prueba con:
   - Nombre: `Punto Feria UD`
   - Dirección: `Cra 7 #40B-53, Bogotá, Colombia`
   - Latitud: `4.6286`
   - Longitud: `-74.0658`
4. Verificar el nuevo punto en la tabla.
5. Centrarlo desde la tabla.
6. Eliminarlo por ID.

### 4.3 Cupones

Permite crear cupones públicos, asignados, cumpleaños y referidos; además habilitar, deshabilitar, consultar y eliminar.

Endpoints usados:

```http
GET /api/coupon/coupons
GET /api/coupon/coupons/code/{code}
GET /api/coupon/coupons/creation-date/{date}
GET /api/coupon/coupons/expiration-date/{date}
GET /api/coupon/coupons/expired
GET /api/coupon/coupons/valid
GET /api/coupon/coupons/enabled
GET /api/coupon/coupons/disabled
GET /api/coupon/coupons/search/{text}
GET /api/coupon/coupons/happy-birthday
GET /api/coupon/coupons/referred
GET /api/coupon/coupons/last/{text}
POST /api/coupon/coupons/unassigned?text={text}&discount={discount}&days={days}
POST /api/coupon/coupons/assigned?text={text}&discount={discount}&days={days}&user_email={email}
POST /api/coupon/coupons/happy-birthday/{user_email}
POST /api/coupon/coupons/referred/{user_email}
POST /api/coupon/coupons/{code}/enable
POST /api/coupon/coupons/{code}/disable
GET /api/coupon/coupons/{code}/is-enabled
DELETE /api/coupon/coupons/{code}
GET /api/coupon/users/{email}/coupons
GET /api/coupon/users/coupons/all
DELETE /api/coupon/users/{email}/coupons/{coupon_code}
```

Caso sugerido:

1. Presionar “Crear casos demo”.
2. Listar cupones.
3. Buscar por texto.
4. Habilitar/deshabilitar un cupón.
5. Consultar cupones del usuario.
6. Probar la aplicación del cupón desde `usuario.html`.

### 4.4 Correos

Permite enviar plantillas a Mailpit usando la API Key local `dev-api-key`.

Endpoints usados:

```http
GET /api/email/health
GET /api/email/emails/health
GET /api/email/email
POST /api/email/emails/auth/register-confirmation
POST /api/email/emails/auth/email-verification
POST /api/email/emails/auth/send-otp
POST /api/email/emails/auth/password-changed
POST /api/email/emails/promotions/discount-available
POST /api/email/emails/promotions/birthday
POST /api/email/emails/promotions/general
POST /api/email/emails/promotions/welcome
POST /api/email/emails/moderation/account-suspended
POST /api/email/emails/moderation/product-rejected
POST /api/email/emails/moderation/policies-updated
POST /api/email/emails/newsletters/news
POST /api/email/emails/newsletters/new-sellers
POST /api/email/emails/referrals/invitation
POST /api/email/emails/referrals/reward
```

Caso sugerido:

1. Seleccionar una plantilla.
2. Enviar correo de prueba.
3. Abrir Mailpit en `http://localhost:8025`.
4. Verificar asunto, destinatario y contenido.

---

## 5. Banco técnico de endpoints

Al final del panel administrador hay dos herramientas:

1. **Matriz de endpoints**: muestra los endpoints detectados por servicio, método y uso.
2. **Ejecutor manual avanzado**: permite probar rutas relativas como `/api/geolocation/geolocation/id/5` o `/api/report/reports/` sin salir del frontend.

Esto permite sustentar el proyecto sin depender de Postman.

---

## 6. Notas importantes

- El mapa requiere internet para descargar tiles de OpenStreetMap.
- Si Leaflet no está disponible, el sistema conserva un mapa visual alternativo con marcadores calculados por coordenadas.
- La búsqueda por nombre y dirección en `geolocation` depende de coincidencias exactas porque así está implementado el servicio.
- El servicio `report` depende de PostgreSQL y Mailpit en Docker.
- El servicio `email` usa `dev-api-key` en entorno local.

## Corrección final del mapa Leaflet

Se agregó una capa de CSS embebida de seguridad para Leaflet dentro de `frontend/styles.css`. Esta capa evita que el mapa se vea como un rompecabezas o por partes cuando el navegador no alcanza a cargar correctamente el CSS externo de Leaflet desde CDN.

La corrección fuerza el comportamiento requerido por Leaflet:

- `.leaflet-pane`, `.leaflet-tile`, `.leaflet-marker-icon` y capas internas quedan en `position: absolute`.
- Las teselas de OpenStreetMap quedan con tamaño real de `256px x 256px` y `max-width: none`.
- El contenedor `.bogota-map` queda con altura estricta y responsive.
- El mapa de usuario y admin comparten la misma configuración visual.
- Se mantiene el fallback estático si `window.L` no está disponible.

Con esto, la vista de geolocalización debe mostrarse como un mapa continuo de Bogotá, no como bloques sueltos.
