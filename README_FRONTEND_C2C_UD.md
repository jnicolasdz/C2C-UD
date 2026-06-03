# Frontend C2C-UD por roles

Este frontend unifica los servicios `report`, `geolocation`, `coupon` y `email` en una interfaz de exposición con estética institucional de la Universidad Distrital: rojo, blanco, tarjetas limpias, formularios de prueba y vistas separadas para usuario y administrador.

## Ejecución

```bash
docker compose up --build
```

Luego abre:

- Frontend: `http://localhost:8080`
- Vista usuario: `http://localhost:8080/usuario.html`
- Vista administrador: `http://localhost:8080/admin.html`
- Mailpit: `http://localhost:8025`

## Vista usuario

La vista de usuario está pensada para simular una experiencia real del marketplace C2C-UD.

### Reportes

Permite radicar reportes con un formulario. El flujo muestra el estado del caso y permite consultar el radicado generado. Se usa para exponer el servicio `report` desde el punto de vista de quien reporta una situación.

### Geolocalización

Muestra un mapa real de Bogotá usando Leaflet y OpenStreetMap. El mapa consume las coordenadas del microservicio `geolocation` y permite:

- Cargar todas las sedes con `GET /geolocation/all_address`.
- Buscar una sede por ID con `GET /geolocation/id/{location_id}`.
- Buscar por nombre con `GET /geolocation/name/{name}`.
- Buscar por dirección con `GET /geolocation/address/{address}`.
- Centrar el mapa en la sede encontrada.
- Ver el marcador con ID, nombre, dirección, latitud y longitud.

El mapa fue corregido con CSS embebido de Leaflet para evitar que se vea cortado o como rompecabezas si el CSS externo no carga bien.

### Cupones

Permite consultar cupones de usuario y probar la aplicación de un descuento con formularios controlados.

## Vista administrador

La vista admin está pensada para sustentar y probar todos los servicios con más control.

### Reportes

Permite listar reportes, crear casos de prueba, revisar estados, filtrar y ejecutar acciones administrativas como reintentos o eliminación cuando el endpoint está disponible.

### Geolocalización

Permite operar directamente los endpoints del servicio:

- `GET /geolocation/all_address`
- `GET /geolocation/id/{location_id}`
- `GET /geolocation/name/{name}`
- `GET /geolocation/address/{address}`
- `POST /geolocation/add/{name}/{description}/{address}/{latitude}/{longitude}`
- `DELETE /geolocation/{location_id}`

La sección incluye mapa real, formulario de búsqueda, formulario de creación y formulario de eliminación.

### Cupones

Permite consultar, crear, habilitar, deshabilitar y probar cupones según los endpoints disponibles del servicio `coupon`.

### Correos

Permite enviar correos de prueba y revisar la salida en Mailpit. Esto permite exponer el servicio `email` sin depender de un correo real externo.

## Corrección del mapa

La versión actual incluye una corrección específica para Leaflet/OpenStreetMap. El problema visto era que las teselas del mapa se dibujaban como imágenes sueltas, con espacios en blanco y partes cortadas. Esto normalmente ocurre cuando el CSS de Leaflet no carga o queda sobreescrito.

La solución aplicada está en `frontend/styles.css` e incluye:

- CSS esencial de Leaflet embebido localmente.
- Posicionamiento absoluto de capas, teselas, marcadores y controles.
- Altura fija responsive para `.bogota-map`.
- Tamaño forzado de teselas `256px x 256px`.
- `max-width: none` para imágenes del mapa.
- `invalidateSize()` desde `frontend/app.js` después de cargar y centrar marcadores.

Con esto el mapa debe verse completo dentro de las dimensiones establecidas.
