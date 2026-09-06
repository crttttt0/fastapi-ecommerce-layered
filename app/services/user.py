from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.exceptions import EntityAlreadyExistsException
from app.core.security import hash_password

if TYPE_CHECKING:
    from app.core.enums import UserRole
    from app.models import User
    from app.repositories import UserRepository


class UserService:
    """Сервис для работы с пользователями: регистрация."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    # Вспомогательные методы

    async def _check_email_is_unique(self, email: str) -> None:
        """
        Проверяет, что email еще не зарегистрирован.
        Если пользователь с таким email существует – выбрасывает исключение.
        """

        db_user = await self.user_repository.get_user_by_email(email)
        if db_user is not None:
            raise EntityAlreadyExistsException(
                f"Пользователь с email {email} уже зарегистрирован."
            )

    # Публичные методы

    async def create_user(self, email: str, password: str, role: UserRole) -> User:
        """Регистрирует нового пользователя с хешированием пароля."""

        await self._check_email_is_unique(email=email)

        return await self.user_repository.create(
            email=email,
            hashed_password=hash_password(password=password),
            role=role,
        )
