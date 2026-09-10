from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ReviewInput(BaseModel):
    """
    Модель для создания отзыва.
    Используется в POST запросах.
    """

    product_id: Annotated[
        int, Field(description="ID товара, к которому относится отзыв")
    ]
    comment: Annotated[
        str | None,
        Field(
            default=None, max_length=500, description="Текст отзыва (до 500 символов)"
        ),
    ]
    grade: Annotated[int, Field(ge=1, le=5, description="Оценка от 1 до 5")]


class ReviewRead(BaseModel):
    """
    Модель для ответа с данными отзыва.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор отзыва")]
    comment: Annotated[str | None, Field(default=None, description="Текст отзыва")]
    comment_date: Annotated[
        datetime, Field(description="Дата и время написания отзыва")
    ]
    grade: Annotated[int, Field(description="Оценка от 1 до 5")]
    is_active: Annotated[bool, Field(description="Активен ли отзыв")]

    user_id: Annotated[int, Field(description="ID пользователя, оставившего отзыв")]
    product_id: Annotated[
        int, Field(description="ID товара, к которому относится отзыв")
    ]

    model_config = ConfigDict(from_attributes=True)
