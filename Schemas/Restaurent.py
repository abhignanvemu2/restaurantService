from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class RestaurantCreate(BaseModel):
    name:  constr(strip_whitespace=True, min_length=1) 
    description: Optional[str] = None

class UpdateRestaurant(BaseModel):
    name:  constr(strip_whitespace=True, min_length=1) 
    description: Optional[str]=None

class UpdateStatus(BaseModel):
    status: int



class RestaurantTrackerResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: int  # 1 -> Online, 0 -> Offline
    created_at: datetime

    class Config:
        orm_mode = True

class RestaurantResponse(RestaurantCreate):
    id: int 

    class Config:
        orm_mode = True
