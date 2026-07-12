from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, Field, computed_field

SchemaType = TypeVar("SchemaType")


class PaginationParameters(BaseModel):
    """
    Модель для параметров пагинации.
    Используется в GET-запросах со списками записей.
    """

    page: Annotated[int, Field(1, ge=1, description="Номер страницы")]
    limit: Annotated[
        int,
        Field(
            25, ge=5, description="Количество записей на одной странице (не менее 5)"
        ),
    ]


class PaginatedResponse(BaseModel, Generic[SchemaType]):
    """
    Модель для ответа с пагинацией. Содержит общее кол-во записей и страниц.
    Используется в GET-запросах со списками записей.
    """

    page: Annotated[int, Field(description="Номер текущей страницы")]
    limit: Annotated[int, Field(description="Количество записей на странице")]
    total: Annotated[int, Field(description="Общее количество записей")]

    @computed_field
    @property
    def pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit if self.limit else 0

    items: Annotated[list[SchemaType], Field(description="Записи")]
