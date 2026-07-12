from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from app.core.exceptions import (
    BusinessRuleViolationException,
    EntityNotFoundException,
    InvalidForeignKeyException,
)

if TYPE_CHECKING:
    from app.models import Category
    from app.repositories import CategoryRepository


class CategoryService:
    """Сервис для работы с категориями: получение, создание, обновление, деактивация."""

    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    # Вспомогательные методы

    async def _get_category_by_id_or_raise(self, category_id: int) -> Category:
        """
        Получает категорию по ID, если не найдена – выбрасывает исключение.
        Вспомогательная функция проверки в функциях сервиса.
        """

        db_category = await self.category_repository.get_by_id(category_id)
        if not db_category:
            raise EntityNotFoundException(
                f"Категория с ID {category_id} не найдена или не активна."
            )

        return db_category

    def _check_parent_id_is_not_category_id(
        self, category_id: int, parent_id: int
    ) -> None:
        """
        Проверяет, что новый parent_id допустим при обновлении категории:
        родитель не совпадает с самой категорией и существует.
        """

        if parent_id == category_id:
            raise BusinessRuleViolationException(
                "Категория не может быть родительской сама для себя."
            )

    async def _check_parent_category_exists(self, parent_id: int) -> None:
        """
        Проверяет существование родительской категории по ID.
        Если родитель не найден – выбрасывает исключение о нарушении внешнего ключа.
        """

        try:
            await self._get_category_by_id_or_raise(category_id=parent_id)
        except EntityNotFoundException:
            raise InvalidForeignKeyException(
                f"Родительская категория с ID {parent_id} не найдена или не активна."
            )

    # Публичные методы

    async def get_all_categories(
        self, page: int, limit: int
    ) -> tuple[Sequence[Category], int]:
        """Возвращает страницу активных категорий с пагинацией и подсчетом записей."""

        items = await self.category_repository.get_all(page, limit)
        total = await self.category_repository.count()

        return items, total

    async def get_category_by_id(self, category_id: int) -> Category:
        """Возвращает категорию по ее ID."""

        return await self._get_category_by_id_or_raise(category_id=category_id)

    async def create_category(
        self, name: str, parent_id: int | None = None
    ) -> Category:
        """Создает новую категорию, проверяя существование родителя, если он указан."""

        if parent_id is not None:
            await self._check_parent_category_exists(parent_id=parent_id)

        return await self.category_repository.create(name=name, parent_id=parent_id)

    async def update_category(
        self, category_id: int, name: str, parent_id: int | None = None
    ) -> Category:
        """Обновляет существующую категорию по ее ID."""

        db_category = await self._get_category_by_id_or_raise(category_id=category_id)
        if parent_id is not None:
            self._check_parent_id_is_not_category_id(
                category_id=category_id, parent_id=parent_id
            )
            await self._check_parent_category_exists(parent_id=parent_id)

        return await self.category_repository.update(
            db_category, name=name, parent_id=parent_id
        )

    async def deactivate_category(self, category_id: int) -> Category:
        """Деактивирует категорию по ее ID (soft delete)."""

        db_category = await self._get_category_by_id_or_raise(category_id=category_id)
        return await self.category_repository.deactivate(db_category)
