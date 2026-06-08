# Pruebas unitarias - Servicio de reportes

Este módulo incluye pruebas unitarias para verificar las historias HU023 a HU027 sin depender del frontend.

## ¿Qué se prueba?

| Historia | Prueba incluida |
|---|---|
| HU023 - Persistencia y gestión | Creación del reporte, ID único, radicado, relación con usuario, filtro por correo y búsqueda exacta por radicado. |
| HU024 - Envío y reintento | Respuesta `success`, `send_status`, `retry_available` y manejo de fallos técnicos de correo. |
| HU025 - Detalles de reporte | Envío de notificación al usuario y al administrador al crear el reporte. |
| HU026 - Notificaciones de estado | Respuestas claras para que el frontend muestre éxito/error y correo cuando el administrador cambia el estado. |
| HU027 - Reintento de fallidos | Reintento conservando el mismo `id` y `radicado`, actualización a `ENVIADO` o permanencia como `FALLIDO`. |

## Ejecutar pruebas dentro del contenedor

Desde la raíz del proyecto `C2C-UD-develop`:

```bash
docker compose run --rm report pytest tests -v
```

## Generar evidencia en XML para entregar al profesor

```bash
docker compose run --rm report pytest tests -v --junitxml=tests/results/report_tests.xml
```

Ese comando deja un archivo en:

```txt
services/report/tests/results/report_tests.xml
```

## Generar reporte de cobertura

```bash
docker compose run --rm report pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml:tests/results/coverage.xml
```

Archivos generados:

```txt
services/report/tests/results/report_tests.xml
services/report/tests/results/coverage.xml
```

## Pruebas principales

- `test_create_report_success_sets_enviado_and_sends_user_and_admin_email`
- `test_create_report_email_failure_marks_fallido_and_allows_retry`
- `test_retry_failed_report_keeps_original_id_and_radicado`
- `test_get_reports_filters_by_user_email_and_excludes_deleted`
- `test_get_report_by_radicado_returns_exact_report_and_user_relation`
- `test_update_status_sends_email_to_user`
- `test_delete_report_is_logical_for_audit`

## Recomendación de entrega

Incluye en el informe o README del proyecto:

1. Captura del comando `pytest tests -v`.
2. Archivo `report_tests.xml` como evidencia automática.
3. Breve tabla relacionando cada historia con sus pruebas.
4. Capturas de Swagger para `POST /reports`, `PUT /reports/{id}` y `POST /reports/{id}/retry`.
