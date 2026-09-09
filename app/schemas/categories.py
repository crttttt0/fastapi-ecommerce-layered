from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CategoryInput(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            description="Название категории (3-50 символов)",
        ),
    ]

    parent_id: Annotated[
        int | None, Field(None, description="ID родительской категории, если есть")
    ]


class CategoryRead(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """

    id: Annotated[int, Field(description="Уникальный идентификатор категории")]
    name: Annotated[str, Field(description="Название категории")]
    is_active: Annotated[bool, Field(description="Активна ли категория")]

    parent_id: Annotated[
        int | None, Field(None, description="ID родительской категории, если есть")
    ]

    model_config = ConfigDict(from_attributes=True)
