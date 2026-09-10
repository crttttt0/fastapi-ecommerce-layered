from app.models import Category

from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями."""

    model = Category
