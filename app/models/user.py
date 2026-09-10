from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import UserRole
from app.database import Base

if TYPE_CHECKING:
    from .product import Product
    from .review import Review


class User(Base):
    """Пользователь"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.buyer)

    products: Mapped[list[Product]] = relationship(
        back_populates="seller", lazy="raise"
    )
    reviews: Mapped[list[Review]] = relationship(back_populates="user", lazy="raise")
