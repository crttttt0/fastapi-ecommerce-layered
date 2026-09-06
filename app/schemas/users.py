from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


class UserInput(BaseModel):
    """
    Модель для создания и обновления пользователя.
    Используется в POST и PUT запросах.
    """

    email: Annotated[EmailStr, Field(description="Email пользователя")]
    password: Annotated[
        str, Field(min_length=8, description="Пароль (минимум 8 символов)")
    ]
    role: Annotated[
        UserRole,
        Field(
            default=UserRole.buyer,
            description="Роль: 'buyer' или 'seller'",
        ),
    ]


class UserRead(BaseModel):
    """
    Модель для ответа с данными пользователя.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор пользователя")]
    email: Annotated[EmailStr, Field(description="Email пользователя")]
    is_active: Annotated[bool, Field(description="Активен ли пользователь")]
    role: Annotated[UserRole, Field(description="Роль: 'buyer' или 'seller'")]

    model_config = ConfigDict(from_attributes=True)
