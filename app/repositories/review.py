from decimal import Decimal
from typing import Sequence

from sqlalchemy import func, select

from app.models import Review

from .base import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Репозиторий для работы с отзывами."""

    model = Review

    async def get_all_by_product_id(
        self, product_id: int, page: int, limit: int
    ) -> Sequence[Review]:
        """Получить страницу отзывов по ID продукта."""

        result = await self.session.scalars(
            select(Review)
            .where(Review.product_id == product_id, Review.is_active)
            .offset(limit * (page - 1))
            .limit(limit)
        )
        return result.all()

    async def count_by_product_id(self, product_id: int) -> int:
        """Подсчитать количество отзывов на продукт"""

        return (
            await self.session.scalar(
                select(func.count())
                .select_from(Review)
                .where(Review.product_id == product_id, Review.is_active)
            )
            or 0
        )

    async def get_average_grade_by_product_id(self, product_id: int) -> Decimal:
        """Получить средний балл активных отзывов по ID продукта."""

        return await self.session.scalar(
            select(func.avg(Review.grade)).where(
                Review.product_id == product_id, Review.is_active
            )
        ) or Decimal("0.00")
