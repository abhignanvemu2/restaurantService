from fastapi import APIRouter
from .Restaurent import router as Restaurent

router = APIRouter()

router.include_router(Restaurent, prefix="/restaurent", tags=['restaurent'])