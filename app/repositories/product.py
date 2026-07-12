from typing import Sequence

from sqlalchemy import func, select

from app.models import Product

from .base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    model = Product

    async def get_all_by_category_id(
        self, category_id: int, page: int, limit: int
    ) -> Sequence[Product]:
        """Получить страницу товаров по ID категории."""

        result = await self.session.scalars(
            select(Product)
            .where(Product.category_id == category_id, Product.is_active)
            .offset(limit * (page - 1))
            .limit(limit)
        )
        return result.all()

    async def count_by_category_id(self, category_id: int) -> int:
        """Подсчитать количество товаров в категории."""

        return (
            await self.session.scalar(
                select(func.count())
                .select_from(Product)
                .where(Product.category_id == category_id, Product.is_active)
            )
            or 0
        )
