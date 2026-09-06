from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_user_service
from app.schemas.users import UserInput, UserRead
from app.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserInput,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    """Регистрирует нового пользователя с ролью 'buyer' или 'seller'."""

    return await user_service.create_user(**user.model_dump())  # type: ignore
