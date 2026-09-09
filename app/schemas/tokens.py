from typing import Annotated

from pydantic import BaseModel, Field


class AccessTokenResponse(BaseModel):
    """Ответ с одним access-токеном."""

    access_token: Annotated[str, Field(description="JWT-токен доступа")]
    token_type: Annotated[
        str, Field("bearer", description="Тип токена (по умолчанию bearer)")
    ]


class RefreshTokenRequest(BaseModel):
    """Тело запроса на обновление пары токенов по refresh-токену."""

    refresh_token: Annotated[str, Field(description="JWT-токен обновления")]


class RefreshTokenResponse(RefreshTokenRequest):
    """Ответ с новым refresh-токеном."""

    token_type: Annotated[
        str, Field("bearer", description="Тип токена (по умолчанию bearer)")
    ]


class TokensResponse(BaseModel):
    """Ответ с парой токенов access и refresh."""

    access_token: Annotated[str, Field(description="JWT-токен доступа")]
    refresh_token: Annotated[str, Field(description="JWT-токен обновления")]
    token_type: Annotated[
        str, Field("bearer", description="Тип токена (по умолчанию bearer)")
    ]
