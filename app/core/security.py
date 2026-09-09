from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from .config import settings
from .exceptions import AuthenticationFailedException

password_hash = PasswordHash.recommended()


# Пароли


def hash_password(password: str) -> str:
    """
    Преобразует пароль в безопасный хеш
    """

    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введенный пароль сохраненному хешу
    """

    return password_hash.verify(plain_password, hashed_password)


# JWT


def create_access_token(data: dict) -> str:
    """Создает подписанный access-токен с claims iat, exp и type=access."""

    payload = data.copy()
    payload.update(
        {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
            "type": "access",
        }
    )

    return jwt.encode(
        payload, settings.jwt.SECRET_KEY.get_secret_value(), settings.jwt.ALGORITHM
    )


def create_refresh_token(data: dict) -> str:
    """Создает подписанный refresh-токен с claims iat, exp и type=refresh."""

    payload = data.copy()
    payload.update(
        {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
            "type": "refresh",
        }
    )

    return jwt.encode(
        payload, settings.jwt.SECRET_KEY.get_secret_value(), settings.jwt.ALGORITHM
    )


def decode_token(token: str) -> dict:
    """Декодирует и проверяет JWT, возвращая claims из payload."""

    try:
        return jwt.decode(
            token,
            settings.jwt.SECRET_KEY.get_secret_value(),
            [settings.jwt.ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailedException("Срок действия токена истек.")
    except jwt.PyJWTError:
        raise AuthenticationFailedException("Не удалось проверить учетные данные.")
