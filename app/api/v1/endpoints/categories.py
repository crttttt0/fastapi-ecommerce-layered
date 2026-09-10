from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import (
    get_category_service,
    get_current_user_with_roles,
)
from app.core.enums import UserRole
from app.schemas.categories import CategoryInput, CategoryRead
from app.schemas.pagination import PaginatedResponse, PaginationParameters
from app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=PaginatedResponse[CategoryRead])
async def get_all_categories(
    pagination: Annotated[PaginationParameters, Depends()],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> PaginatedResponse[CategoryRead]:
    """Возвращает список всех категорий товаров. Доступно всем, в т.ч. без аутентификации."""

    items, count = await category_service.get_all_categories(**pagination.model_dump())

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@router.post(
    "/",
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_with_roles(UserRole.admin))],
)
async def create_category(
    category: CategoryInput,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """Создает новую категорию. Доступно только 'admin'."""

    return await category_service.create_category(**category.model_dump())  # type: ignore


@router.put(
    "/{category_id}",
    response_model=CategoryRead,
    dependencies=[Depends(get_current_user_with_roles(UserRole.admin))],
)
async def update_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории, больше 0")],
    category: CategoryInput,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """
    Обновляет категорию по ее ID.
    Доступно только 'admin'.
    """

    return await category_service.update_category(
        category_id=category_id, **category.model_dump()
    )  # type: ignore


@router.delete(
    "/{category_id}",
    response_model=CategoryRead,
    dependencies=[Depends(get_current_user_with_roles(UserRole.admin))],
)
async def delete_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории, больше 0")],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """Удаляет категорию по ее ID. Доступно только 'admin'."""

    return await category_service.deactivate_category(category_id=category_id)  # type: ignore
