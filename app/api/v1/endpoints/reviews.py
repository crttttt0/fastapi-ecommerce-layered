from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import (
    get_current_user_with_roles,
    get_review_service,
)
from app.core.enums import UserRole
from app.models import User
from app.schemas.pagination import PaginatedResponse, PaginationParameters
from app.schemas.reviews import ReviewInput, ReviewRead
from app.services import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])
product_reviews_router = APIRouter(tags=["reviews", "products"])


@router.get("/", response_model=PaginatedResponse[ReviewRead])
async def get_all_reviews(
    pagination: Annotated[PaginationParameters, Depends()],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
) -> PaginatedResponse[ReviewRead]:
    """Возвращает список всех отзывов. Доступно всем, в т.ч. без аутентификации."""

    items, count = await review_service.get_all_reviews(**pagination.model_dump())

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@product_reviews_router.get(
    "/products/{product_id}/reviews/", response_model=PaginatedResponse[ReviewRead]
)
async def get_product_reviews(
    product_id: Annotated[int, Path(ge=1, description="ID продукта, больше 0")],
    pagination: Annotated[PaginationParameters, Depends()],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
) -> PaginatedResponse[ReviewRead]:
    """Возвращает список отзывов о конкретном товаре по его ID. Доступно всем, в т.ч. без аутентификации."""

    items, count = await review_service.get_all_reviews_by_product_id(
        product_id=product_id, **pagination.model_dump()
    )

    return PaginatedResponse(**pagination.model_dump(), total=count, items=items)  # type: ignore


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review(
    current_user: Annotated[User, Depends(get_current_user_with_roles(UserRole.buyer))],
    review: ReviewInput,
    review_service: Annotated[ReviewService, Depends(get_review_service)],
) -> ReviewRead:
    """Создает новый отзыв о товаре и пересчитывает рейтинг. Доступно только 'buyer'."""

    return await review_service.create_review(
        current_user=current_user, **review.model_dump()
    )  # type: ignore


@router.delete("/{review_id}", response_model=ReviewRead)
async def delete_review(
    current_user: Annotated[
        User, Depends(get_current_user_with_roles(UserRole.buyer, UserRole.admin))
    ],
    review_id: Annotated[int, Path(ge=1, description="ID отзыва, больше 0")],
    review_service: Annotated[ReviewService, Depends(get_review_service)],
) -> ReviewRead:
    """Выполняет мягкое удаление отзыва. Доступно автору отзыва или 'admin'."""

    return await review_service.deactivate_review(
        current_user=current_user, review_id=review_id
    )
