from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.v1.routes import router

app = FastAPI(title="Email Service")


def _error_response(
	error_code: str,
	message: str,
	correlation_id: str | None = None,
	details: list[object] | None = None,
) -> dict[str, object | None]:
	return {
		"success": False,
		"error_code": error_code,
		"message": message,
		"details": details,
		"correlation_id": correlation_id,
	}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
	if isinstance(exc.detail, dict) and "success" in exc.detail:
		return JSONResponse(status_code=exc.status_code, content=exc.detail)

	error_code = "SRV_001"
	message = "Error interno inesperado del servidor."
	if exc.status_code == 401:
		error_code = "AUTH_001"
		message = "API Key ausente o inválida."

	return JSONResponse(
		status_code=exc.status_code,
		content=_error_response(error_code, message),
	)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
	errors = exc.errors()
	error_code = "VAL_002"
	if any(error.get("type", "").startswith("missing") for error in errors):
		error_code = "VAL_002"
	else:
		error_code = "VAL_003"

	details = [
		{
			"loc": error.get("loc"),
			"msg": error.get("msg"),
			"type": error.get("type"),
		}
		for error in errors
	]

	return JSONResponse(
		status_code=400,
		content=_error_response(error_code, "El body del request está vacío o mal formado.", details=details),
	)


app.include_router(router, prefix="/api/v1")
