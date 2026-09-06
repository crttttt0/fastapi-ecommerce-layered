from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .category import Category
    from .user import User


class Product(Base):
    """Товар"""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(String(200))
    stock: Mapped[int] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    category: Mapped[Category] = relationship(back_populates="products", lazy="raise")
    seller: Mapped[User] = relationship(back_populates="products", lazy="raise")
