from fastapi import APIRouter

from .endpoints import (
    categories_router,
    product_reviews_router,
    products_router,
    reviews_router,
    users_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(users_router)
api_router.include_router(reviews_router)
api_router.include_router(product_reviews_router)
