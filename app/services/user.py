from __future__ import annotations

from typing import TYPE_CHECKING

from app.core.exceptions import (
    AuthenticationFailedException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

if TYPE_CHECKING:
    from app.core.enums import UserRole
    from app.models import User
    from app.repositories import UserRepository


class UserService:
    """Сервис для работы с пользователями: регистрация, логин."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    # Вспомогательные методы

    async def _get_by_email_or_raise(self, email: str) -> User:
        """
        Получает пользователя по email, если не найден – выбрасывает исключение.
        Вспомогательная функция проверки в функциях сервиса.
        """

        db_user = await self.user_repository.get_user_by_email(email)
        if not db_user:
            raise EntityNotFoundException(
                f"Пользователь с email {email} не найден или не активен."
            )

        return db_user

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

    async def _authenticate(self, email: str, password: str) -> User:
        """Аутентифицирует пользователя по email и паролю."""

        try:
            db_user = await self._get_by_email_or_raise(email=email)
        except EntityNotFoundException:
            raise AuthenticationFailedException("Неправильный логин или пароль.")

        if not verify_password(password, db_user.hashed_password):
            raise AuthenticationFailedException("Неправильный логин или пароль.")

        return db_user

    def _issue_access_token(self, user: User) -> dict[str, str]:
        """Выпускает access-токен для пользователя."""

        return {
            "access_token": create_access_token(
                {"sub": user.email, "role": user.role, "id": user.id}
            )
        }

    def _issue_refresh_token(self, user: User) -> dict[str, str]:
        """Выпускает refresh-токен для пользователя."""

        return {
            "refresh_token": create_refresh_token(
                {"sub": user.email, "role": user.role, "id": user.id}
            )
        }

    def _issue_tokens(self, user: User) -> dict[str, str]:
        """Выпускает пару access и refresh токенов."""

        return {
            **self._issue_access_token(user=user),
            **self._issue_refresh_token(user=user),
        }

    # Публичные методы

    async def get_by_email(self, email: str) -> User:
        """Возвращает пользователя по его email."""

        return await self._get_by_email_or_raise(email)

    async def register_user(self, email: str, password: str, role: UserRole) -> User:
        """Регистрирует нового пользователя с хешированием пароля."""

        await self._check_email_is_unique(email=email)

        return await self.user_repository.create(
            email=email,
            hashed_password=hash_password(password=password),
            role=role,
        )

    async def login(self, email: str, password: str) -> dict[str, str]:
        """Аутентифицирует пользователя и возвращает пару access и refresh токенов."""

        db_user = await self._authenticate(email=email, password=password)
        return self._issue_tokens(user=db_user)

    async def refresh_token(self, refresh_token: str) -> dict[str, str]:
        """Выпускает новый refresh-токен на основе переданного, проверяя пользователя в БД."""

        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationFailedException("Неверный тип токена.")

        try:
            user = await self._get_by_email_or_raise(payload.get("sub"))
        except EntityNotFoundException:
            raise AuthenticationFailedException("Пользователь не найден.")

        return self._issue_refresh_token(user=user)

    async def access_token(self, refresh_token: str) -> dict[str, str]:
        """Выпускает новый access-токен на основе переданного refresh-токена, проверяя пользователя в БД."""

        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationFailedException("Неверный тип токена.")

        try:
            user = await self._get_by_email_or_raise(payload.get("sub"))
        except EntityNotFoundException:
            raise AuthenticationFailedException("Пользователь не найден.")

        return self._issue_access_token(user=user)
