from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    """Категория товаров"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(default=True)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped[Category | None] = relationship(
        remote_side="Category.id", back_populates="children", lazy="raise"
    )
    children: Mapped[list[Category]] = relationship(
        back_populates="parent", lazy="raise"
    )
    products: Mapped[list[Product]] = relationship(
        back_populates="category", lazy="raise"
    )
