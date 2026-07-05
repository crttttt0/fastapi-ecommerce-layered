from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

tags_metadata = [
    {"name": "health", "description": "Проверка работоспособности сервера"}
]


def create_app() -> FastAPI:
    """
    Содает экззепляр приложения с настройками из app/core/config.py
    и эндпойнтомм проверки состояния сервера.
    """

    app = FastAPI(
        debug=settings.app.DEBUG,
        title=settings.app.NAME,
        version=settings.app.VERSION,
        openapi_tags=tags_metadata,
    )

    app.include_router(api_router)

    @app.get("/health", tags=["health"], summary="Проверить работоспособность")
    def check_health() -> dict:
        return {"status": "Ок"}

    return app


app = create_app()
