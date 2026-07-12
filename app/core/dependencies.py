from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.repositories import CategoryRepository, ProductRepository
from app.services import CategoryService, ProductService

# Репозитории


async def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryRepository:
    """Возвращает репозиторий для работы с категориями."""

    return CategoryRepository(session=session)


async def get_product_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductRepository:
    """Возвращает репозиторий для работы с товарами."""

    return ProductRepository(session=session)


# Сервисы


async def get_category_service(
    category_repository: Annotated[
        CategoryRepository, Depends(get_category_repository)
    ],
) -> CategoryService:
    """Возвращает сервис для работы с категориями."""

    return CategoryService(category_repository=category_repository)


async def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ProductService:
    """Возвращает сервис для работы с товарами, использующий сервис категорий для валидации."""

    return ProductService(
        product_repository=product_repository, category_service=category_service
    )
