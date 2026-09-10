from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Sequence

from app.core.enums import UserRole
from app.core.exceptions import (
    AccessDeniedException,
    EntityNotFoundException,
    InvalidForeignKeyException,
)

if TYPE_CHECKING:
    from app.models import Review, User
    from app.repositories import ReviewRepository
    from app.services import ProductService


class ReviewService:
    """Сервис для работы с отзывами: получение, создание, деактивация."""

    def __init__(
        self, review_repository: ReviewRepository, product_service: ProductService
    ):
        self.review_repository = review_repository
        self.product_service = product_service

    # Вспомогательные методы

    async def _get_by_id_or_raise(self, review_id: int) -> Review:
        """
        Получает отзыв по ID, если не найден – выбрасывает исключение.
        Вспомогательная функция проверки в функциях сервиса.
        """

        db_review = await self.review_repository.get_by_id(review_id)
        if not db_review:
            raise EntityNotFoundException(
                f"Отзыв с ID {review_id} не найден или неактивен."
            )

        return db_review

    async def _check_product_exists(self, product_id: int) -> None:
        """
        Проверяет существование товара по ID через ProductService.
        Если товар не найден – выбрасывает исключение о нарушении внешнего ключа.
        """

        try:
            await self.product_service.get_product_by_id(product_id=product_id)
        except EntityNotFoundException:
            raise InvalidForeignKeyException(
                f"Продукт с ID {product_id} не найден или не активен."
            )

    async def _update_product_rating_by_id(self, product_id: int) -> None:
        """Пересчитывает и сохраняет средний рейтинг товара по активным отзывам."""

        rating = (
            await self.review_repository.get_average_grade_by_product_id(product_id)
        ).quantize(Decimal("0.01"))

        await self.product_service.update_product_rating(
            product_id=product_id, rating=rating
        )

    # Публичные методы

    async def get_all_reviews(
        self, page: int, limit: int
    ) -> tuple[Sequence[Review], int]:
        """Возвращает страницу активных отзывов с пагинацией и подсчетом записей."""

        items = await self.review_repository.get_all(page, limit)
        total = await self.review_repository.count()

        return items, total

    async def get_all_reviews_by_product_id(
        self, product_id: int, page: int, limit: int
    ) -> tuple[Sequence[Review], int]:
        """Возвращает страницу активных отзывов указанного товара с пагинацией и подсчетом записей."""

        await self.product_service.get_product_by_id(product_id=product_id)

        items = await self.review_repository.get_all_by_product_id(
            product_id, page, limit
        )
        total = await self.review_repository.count_by_product_id(product_id)

        return items, total

    async def create_review(
        self,
        current_user: User,
        product_id: int,
        grade: int,
        comment: str | None = None,
    ) -> Review:
        """Создает новый отзыв, проверяя существование указанного товара."""

        await self._check_product_exists(product_id=product_id)

        db_review = await self.review_repository.create(
            product_id=product_id, user_id=current_user.id, grade=grade, comment=comment
        )
        await self._update_product_rating_by_id(product_id=product_id)

        return db_review

    async def deactivate_review(self, current_user: User, review_id: int) -> Review:
        """Деактивирует отзыв по его ID (soft delete)."""

        db_review = await self._get_by_id_or_raise(review_id=review_id)

        if current_user.id != db_review.user_id and current_user.role != UserRole.admin:
            raise AccessDeniedException("Можно удалять только свой отзыв")

        await self.review_repository.deactivate(db_review)
        await self._update_product_rating_by_id(product_id=db_review.product_id)

        return db_review
