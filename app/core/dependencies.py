from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.exceptions import (
    AccessDeniedException,
    AuthenticationFailedException,
    EntityNotFoundException,
)
from app.core.security import decode_token
from app.database import get_session
from app.models import User
from app.repositories import (
    CategoryRepository,
    ProductRepository,
    ReviewRepository,
    UserRepository,
)
from app.services import CategoryService, ProductService, ReviewService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# Репозитории


async def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CategoryRepository:
    """Возвращает репозиторий для работы с категориями."""

    return CategoryRepository(session=session)


async def get_product_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProductRepository:
    """Возвращает репозиторий для работы с товарами."""

    return ProductRepository(session=session)


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    """Возвращает репозиторий для работы с пользователями."""

    return UserRepository(session=session)


async def get_review_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ReviewRepository:
    """Возвращает репозиторий для работы с отзывами."""

    return ReviewRepository(session=session)


# Сервисы


async def get_category_service(
    category_repository: Annotated[
        CategoryRepository, Depends(get_category_repository)
    ],
) -> CategoryService:
    """Возвращает сервис для работы с категориями."""

    return CategoryService(category_repository=category_repository)


async def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
) -> ProductService:
    """Возвращает сервис для работы с товарами, использующий сервис категорий для валидации."""

    return ProductService(
        product_repository=product_repository, category_service=category_service
    )


async def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """Возвращает сервис для работы с пользователями."""

    return UserService(user_repository=user_repository)


async def get_review_service(
    review_repository: Annotated[ReviewRepository, Depends(get_review_repository)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
) -> ReviewService:
    """Возвращает сервис для работы с отзывами."""

    return ReviewService(
        review_repository=review_repository, product_service=product_service
    )


# JWT


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Возвращает текущего аутентифицированного пользователя по access-токену."""

    if token is None:
        raise AuthenticationFailedException("Токен не предоставлен.")

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise AuthenticationFailedException("Неверный тип токена.")

    try:
        user = await user_service.get_by_email(payload.get("sub"))
    except EntityNotFoundException:
        raise AuthenticationFailedException("Пользователь не найден или неактивен.")

    return user


def get_current_user_with_roles(*roles: UserRole):
    """
    Возвращает зависимость, которая требует, чтобы у текущего пользователя
    была одна из переданных ролей.
    """

    async def get_current_user_with_role(
        user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if user.role not in roles:
            allowed_roles = ", ".join(role.value for role in roles)
            raise AccessDeniedException(
                f"Действие доступно только пользователям с правами: {allowed_roles}"
            )

        return user

    return get_current_user_with_role
