from .categories import router as categories_router
from .products import router as products_router
from .reviews import product_reviews_router
from .reviews import router as reviews_router
from .users import router as users_router

__all__ = [
    "categories_router",
    "product_reviews_router",
    "products_router",
    "reviews_router",
    "users_router",
]
