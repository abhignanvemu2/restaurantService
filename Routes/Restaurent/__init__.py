from fastapi import APIRouter
from .Post import router as create_restaurant 
from .Put import router as update_restaurent
from .Patch import router as update_status
from .AddMenu import router as addMenu
from .availableRestaurents import router as Available
from .RestaurentTracker import router as restaurentTracker 
from .UpdateMenu import router as updateMenu

router = APIRouter()

router.include_router(create_restaurant)
router.include_router(update_restaurent)
router.include_router(updateMenu)
router.include_router(addMenu)
router.include_router(Available)
router.include_router(restaurentTracker)

