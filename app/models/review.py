from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from .product import Product
    from .user import User


class Review(Base):
    """Отзыв"""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str | None] = mapped_column(String(500))
    comment_date: Mapped[datetime] = mapped_column(default=datetime.now)
    grade: Mapped[int] = mapped_column(
        CheckConstraint("grade BETWEEN 1 AND 5", name="ck_reviews_grade_range")
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    user: Mapped[User] = relationship(back_populates="reviews", lazy="raise")
    product: Mapped[Product] = relationship(back_populates="reviews", lazy="raise")
