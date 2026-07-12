from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import get_category_service
from app.schemas.categories import CategoryInput, CategoryRead
from app.schemas.pagination import PaginatedResponse, PaginationParameters
from app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=PaginatedResponse[CategoryRead])
async def get_all_categories(
    pagination: Annotated[PaginationParameters, Depends()],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> PaginatedResponse[CategoryRead]:
    """Возвращает список всех категорий товаров."""

    items, count = await category_service.get_all_categories(**pagination.model_dump())

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryInput,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """Создает новую категорию."""

    return await category_service.create_category(**category.model_dump())  # type: ignore


@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории, больше 0")],
    category: CategoryInput,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """
    Обновляет категорию по ее ID.
    """

    return await category_service.update_category(
        category_id=category_id, **category.model_dump()
    )  # type: ignore


@router.delete("/{category_id}", response_model=CategoryRead)
async def delete_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории, больше 0")],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> CategoryRead:
    """Удаляет категорию по ее ID."""

    return await category_service.deactivate_category(category_id=category_id)  # type: ignore
