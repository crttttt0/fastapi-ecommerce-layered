from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import get_current_user_with_roles, get_product_service
from app.core.enums import UserRole
from app.models import User
from app.schemas.pagination import PaginatedResponse, PaginationParameters
from app.schemas.products import ProductInput, ProductRead
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=PaginatedResponse[ProductRead])
async def get_all_products(
    pagination: Annotated[PaginationParameters, Depends()],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> PaginatedResponse[ProductRead]:
    """Возвращает список всех товаров. Доступно всем, в т.ч. без аутентификации."""

    items, count = await product_service.get_all_products(**pagination.model_dump())

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@router.get("/category/{category_id}", response_model=PaginatedResponse[ProductRead])
async def get_products_by_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории, больше 0")],
    pagination: Annotated[PaginationParameters, Depends()],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> PaginatedResponse[ProductRead]:
    """Возвращает список товаров в указанной категории по ее ID. Доступно всем, в т.ч. без аутентификации."""

    items, count = await product_service.get_all_products_by_category_id(
        category_id=category_id, **pagination.model_dump()
    )

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: Annotated[int, Path(ge=1, description="ID продукта, больше 0")],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductRead:
    """Возвращает детальную информацию о товаре по его ID. Доступно всем, в т.ч. без аутентификации."""

    return await product_service.get_product_by_id(product_id=product_id)  # type: ignore


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    current_user: Annotated[
        User, Depends(get_current_user_with_roles(UserRole.seller))
    ],
    product: ProductInput,
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductRead:
    """Создает новый товар, привязанный к текущему продавцу. Доступно только 'seller'."""

    return await product_service.create_product(
        current_user=current_user, **product.model_dump()
    )  # type: ignore


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    current_user: Annotated[
        User, Depends(get_current_user_with_roles(UserRole.seller))
    ],
    product_id: Annotated[int, Path(ge=1, description="ID продукта, больше 0")],
    product: ProductInput,
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductRead:
    """Обновляет товар по его ID, если он принадлежит текущему продавцу. Доступно только 'seller' (владельцу товара)."""

    return await product_service.update_product(
        current_user=current_user, product_id=product_id, **product.model_dump()
    )  # type: ignore


@router.delete("/{product_id}", response_model=ProductRead)
async def delete_product(
    current_user: Annotated[
        User, Depends(get_current_user_with_roles(UserRole.seller))
    ],
    product_id: Annotated[int, Path(ge=1, description="ID продукта, больше 0")],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductRead:
    """Удаляет товар по его ID (soft delete), если он принадлежит текущему продавцу. Доступно только 'seller' (владельцу товара)."""

    return await product_service.deactivate_product(
        current_user=current_user, product_id=product_id
    )  # type: ignore
