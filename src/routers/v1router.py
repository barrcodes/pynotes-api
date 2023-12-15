from fastapi import APIRouter
from .v1 import notebooks

router = APIRouter(
    prefix="/v1"
)

router.include_router(notebooks.router)
