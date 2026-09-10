from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_user_service
from app.schemas.tokens import (
    AccessTokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    TokensResponse,
)
from app.schemas.users import UserInput, UserRead
from app.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserInput,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Регистрирует нового пользователя с ролью `buyer` или `seller`. Доступно всем."""

    return await user_service.register_user(**user.model_dump())  # type: ignore


@router.post("/login", response_model=TokensResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> TokensResponse:
    """Возвращает пару access и refresh токенов после успешного логина. Доступно всем."""

    return await user_service.login(form_data.username, form_data.password)  # type: ignore


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh(
    data: RefreshTokenRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> RefreshTokenResponse:
    """Выпускает новый refresh-токен по переданному. Доступно всем (по refresh-токену)."""

    return await user_service.refresh_token(data.refresh_token)  # type: ignore


@router.post("/access", response_model=AccessTokenResponse)
async def access(
    data: RefreshTokenRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AccessTokenResponse:
    """Выпускает новый access-токен по refresh-токену. Доступно всем (по refresh-токену)."""

    return await user_service.access_token(data.refresh_token)  # type: ignore
