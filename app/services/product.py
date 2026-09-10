from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from app.core.exceptions import (
    AccessDeniedException,
    EntityNotFoundException,
    InvalidForeignKeyException,
)

if TYPE_CHECKING:
    from decimal import Decimal

    from app.models import Product, User
    from app.repositories import ProductRepository

    from .category import CategoryService


class ProductService:
    """Сервис для работы с товарами: получение, создание, обновление, деактивация."""

    def __init__(
        self, product_repository: ProductRepository, category_service: CategoryService
    ) -> None:
        self.product_repository = product_repository
        self.category_service = category_service

    # Вспомогательные методы

    async def _get_product_by_id_or_raise(self, product_id: int) -> Product:
        """
        Получает товар по ID, если не найден – выбрасывает исключение.
        Вспомогательная функция проверки в функциях сервиса.
        """

        db_product = await self.product_repository.get_by_id(product_id)
        if not db_product:
            raise EntityNotFoundException(
                f"Продукт с ID {product_id} не найден или не активен."
            )

        return db_product

    async def _check_category_exists(self, category_id: int) -> None:
        """
        Проверяет существование категории по ID через CategoryService.
        Если категория не найдена – выбрасывает исключение о нарушении внешнего ключа.
        """

        try:
            await self.category_service.get_category_by_id(category_id=category_id)
        except EntityNotFoundException:
            raise InvalidForeignKeyException(
                f"Категория с ID {category_id} не найдена или не активна."
            )

    # Публичные методы

    async def get_all_products(
        self, page: int, limit: int
    ) -> tuple[Sequence[Product], int]:
        """Возвращает страницу активных товаров с пагинацией и подсчетом записей."""

        items = await self.product_repository.get_all(page, limit)
        count = await self.product_repository.count()

        return items, count

    async def get_all_products_by_category_id(
        self, category_id: int, page: int, limit: int
    ) -> tuple[Sequence[Product], int]:
        """Возвращает страницу активных товаров указанной категории с пагинацией и подсчетом записей."""

        await self.category_service.get_category_by_id(category_id=category_id)
        items = await self.product_repository.get_all_by_category_id(
            category_id, page, limit
        )
        count = await self.product_repository.count_by_category_id(category_id)

        return items, count

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Возвращает товар по его ID, проверяя существование
        активной категории, к которой он относится.
        """

        db_product = await self._get_product_by_id_or_raise(product_id=product_id)
        await self._check_category_exists(category_id=db_product.category_id)

        return db_product

    async def create_product(
        self,
        current_user: User,
        name: str,
        price: Decimal,
        stock: int,
        category_id: int,
        description: str | None = None,
        image_url: str | None = None,
    ) -> Product:
        """Создает новый товар, проверяя существование указанной категории."""

        await self._check_category_exists(category_id=category_id)

        return await self.product_repository.create(
            name=name,
            price=price,
            stock=stock,
            category_id=category_id,
            seller_id=current_user.id,
            description=description,
            image_url=image_url,
        )

    async def update_product(
        self,
        current_user: User,
        product_id: int,
        name: str,
        price: Decimal,
        stock: int,
        category_id: int,
        description: str | None = None,
        image_url: str | None = None,
    ) -> Product:
        """Обновляет существующий товар, проверяя существование указанной категории."""

        db_product = await self._get_product_by_id_or_raise(product_id=product_id)

        if db_product.seller_id != current_user.id:
            raise AccessDeniedException("Можно редактировать только свои продукты")

        await self._check_category_exists(category_id=category_id)

        return await self.product_repository.update(
            db_product,
            name=name,
            price=price,
            stock=stock,
            category_id=category_id,
            description=description,
            image_url=image_url,
        )

    async def update_product_rating(self, product_id: int, rating: Decimal) -> None:
        """Обновляет рейтинг товара по его ID."""

        db_product = await self._get_product_by_id_or_raise(product_id=product_id)
        return await self.product_repository.update(db_product, rating=rating)

    async def deactivate_product(self, current_user: User, product_id: int) -> Product:
        """Деактивирует товар по его ID (soft delete)."""

        db_product = await self._get_product_by_id_or_raise(product_id=product_id)

        if db_product.seller_id != current_user.id:
            raise AccessDeniedException("Можно удалять только свои продукты")

        return await self.product_repository.deactivate(db_product)
