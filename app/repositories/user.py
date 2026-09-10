from sqlalchemy import select

from app.models import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Репозиторий для работы с пользователями."""

    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        """Получить активного пользователя по email."""

        return await self.session.scalar(
            select(User).where(User.email == email, User.is_active)
        )
