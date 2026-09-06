from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    BusinessRuleViolationException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    InvalidForeignKeyException,
)

tags_metadata = [
    {"name": "health", "description": "Проверка работоспособности сервера"}
]


def create_app() -> FastAPI:
    """
    Создает экземпляр приложения с настройками из app/core/config.py
    и эндпоинтом проверки состояния сервера.
    """

    app = FastAPI(
        debug=settings.app.DEBUG,
        title=settings.app.NAME,
        version=settings.app.VERSION,
        openapi_tags=tags_metadata,
    )

    @app.exception_handler(InvalidForeignKeyException)
    async def invalid_foreign_key_handler(
        request: Request, exc: InvalidForeignKeyException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.detail}
        )

    @app.exception_handler(BusinessRuleViolationException)
    async def business_rule_violation_handler(
        request: Request, exc: BusinessRuleViolationException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.detail}
        )

    @app.exception_handler(EntityNotFoundException)
    async def entity_not_found_handler(
        request: Request, exc: EntityNotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.detail}
        )

    @app.exception_handler(EntityAlreadyExistsException)
    async def entity_already_exists_handler(
        request: Request, exc: EntityAlreadyExistsException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": exc.detail}
        )

    app.include_router(api_router)

    @app.get("/health", tags=["health"], summary="Проверить работоспособность")
    def check_health() -> dict:
        return {"status": "Ок"}

    return app


app = create_app()
