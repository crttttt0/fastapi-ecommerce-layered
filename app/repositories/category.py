from app.models import Category

from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    model = Category
