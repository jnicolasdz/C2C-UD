# Estructura del Proyecto C2C-UD

Este documento describe la estructura del proyecto y la función de cada archivo y carpeta, con el objetivo de proporcionar una guía técnica para el equipo de desarrollo.

## Estructura General

El proyecto está organizado en las siguientes carpetas principales:

```
C2C-UD/
├── services/
├── scripts/
├── infra/
├── shared/
├── docker-compose.yml
```

### 1. `services/`
Contiene los microservicios del proyecto. Cada microservicio tiene una estructura similar, diseñada para ser modular y escalable. Los microservicios disponibles son: `coupon`, `email`, `geolocation` y `report`.

#### Estructura de un microservicio
```
service_name/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── tests/
│   └── test_health.py
```

- **`Dockerfile`**: Define la configuración para construir la imagen Docker del microservicio.
- **`requirements.txt`**: Lista las dependencias necesarias para el microservicio.
- **`app/`**: Contiene el código fuente del microservicio.
    - **`main.py`**: Punto de entrada del microservicio.
    - **`api/`**: Define las rutas y controladores de la API.
        - **`v1/routes.py`**: Contiene las rutas de la versión 1 de la API.
    - **`core/config.py`**: Configuración central del microservicio.
    - **`models/`**, **`schemas/`**, **`services/`**: Directorios para modelos, esquemas y lógica de negocio.
- **`tests/`**: Contiene pruebas unitarias y de integración.
    - **`test_health.py`**: Prueba de salud del microservicio.

### 2. `scripts/`
Carpeta destinada a scripts auxiliares o automatizaciones. Actualmente está vacía, pero puede ser utilizada para tareas como migraciones, generación de datos, etc.

### 3. `infra/`
Contiene configuraciones relacionadas con la infraestructura del proyecto.

- **`nginx/nginx.conf`**: Archivo de configuración para el servidor Nginx, utilizado como proxy inverso o balanceador de carga.

### 4. `shared/`
Contiene código compartido entre los microservicios.

- **`__init__.py`**: Indica que el directorio es un módulo Python.
- **`utils/`**: Contiene utilidades y funciones comunes.
    - **`__init__.py`**: Archivo de inicialización del módulo.

### 5. `docker-compose.yml`
Archivo de configuración para orquestar los microservicios con Docker Compose. Define los servicios, puertos, volúmenes y variables de entorno.

#### Servicios definidos:
- **`coupon_service`**: Microservicio de cupones, expuesto en el puerto `8001`.
- **`email_service`**: Microservicio de correos electrónicos, expuesto en el puerto `8002`.
- **`geolocation_service`**: Microservicio de geolocalización, expuesto en el puerto `8003`.
- **`report_service`**: Microservicio de reportes, expuesto en el puerto `8004`.

Cada servicio monta su código fuente como volumen para facilitar el desarrollo.

---

Esta estructura modular permite un desarrollo organizado, escalable y fácil de mantener. Si tienes dudas, consulta con el equipo técnico.  

---

### 6. ¿Cómo desplegar el proyecto?

Por medio de `docker-compose` se orquesta la creación y despliegue de los contenedores con el comando `docker compose up --build` y ejecutar directamente de la raíz del proyecto. 