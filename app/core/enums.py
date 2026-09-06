from enum import Enum


class UserRole(str, Enum):
    """Роль пользователя"""

    buyer = "buyer"
    seller = "seller"
