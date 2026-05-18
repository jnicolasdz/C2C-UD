# C2C-UD: Proyecto FastAPI Orientado a Microservicios  

Este proyecto está desarrollado utilizando **FastAPI**, un framework moderno y de alto rendimiento para construir APIs con Python. La estructura del proyecto está diseñada para seguir un enfoque modular y orientado a microservicios, lo que facilita la escalabilidad, el mantenimiento y la colaboración en equipo.  

## Estructura del Proyecto  

A continuación, se describe la función de cada carpeta en el proyecto:  

### **app/**  
Contiene el código principal de la aplicación.  

- **`__init__.py`**: Marca el directorio como un paquete Python.  
- **`dependencies.py`**: Define dependencias comunes que pueden ser inyectadas en los endpoints.  
- **`main.py`**: Punto de entrada de la aplicación. Contiene la configuración inicial y el arranque del servidor FastAPI.  

#### **core/**  
Contiene la configuración y lógica central del proyecto.  

- **`config.py`**: Configuración de variables de entorno y parámetros globales.  
- **`security.py`**: Implementación de mecanismos de seguridad, como autenticación y autorización.  

#### **db/**  
Gestión de la base de datos.  

- **`database.py`**: Configuración de la conexión a la base de datos y manejo de sesiones.  

#### **internal/**  
Lógica interna y funcionalidades administrativas.  

- **`admin.py`**: Funciones administrativas internas no expuestas públicamente.  

#### **models/**  
Definición de los modelos de datos utilizados en la aplicación.  

- **`__init__.py`**: Inicialización del paquete de modelos.  

#### **routers/**  
Definición de los endpoints de la API.  

- **`coupons.py`**: Endpoints relacionados con cupones.  
- **`email.py`**: Endpoints para el manejo de correos electrónicos.  
- **`geolocation.py`**: Endpoints para servicios de geolocalización.  
- **`report.py`**: Endpoints para generación de reportes.  

#### **schemas/**  
Definición de los esquemas de datos (Pydantic) utilizados para validación y serialización.  

- **`__init__.py`**: Inicialización del paquete de esquemas.  

#### **services/**  
Implementación de la lógica de negocio dividida en submódulos.  

- **`coupon_service/`**: Lógica relacionada con cupones.  
    - **`coupon_service.py`**: Funciones específicas para el manejo de cupones.  
- **`email_service/`**: Lógica para el envío de correos electrónicos.  
    - **`email_service.py`**: Funciones específicas para el manejo de correos.  
- **`geolocation_service/`**: Lógica para servicios de geolocalización.  
    - **`geolocation_service.py`**: Funciones específicas para geolocalización.  
- **`report_service/`**: Lógica para generación de reportes.  
    - **`report_service.py`**: Funciones específicas para reportes.  

### **tests/**  
Contiene los archivos de pruebas para garantizar la calidad y el correcto funcionamiento de la aplicación.  

- **`__init__.py`**: Inicialización del paquete de pruebas.  

## Cómo Ejecutar el Proyecto  

1. Clona el repositorio.  
2. Instala las dependencias necesarias utilizando `pip install -r requirements.txt`.  
3. Configura las variables de entorno necesarias en un archivo `.env`.  
4. Ejecuta la aplicación con el siguiente comando:  
     ```bash  
     uvicorn app.main:app --reload  
     ```  
5. Accede a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.  


