from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.RestaurentModel import Restaurant
from Schemas.Restaurent import RestaurantCreate, RestaurantResponse
from Models.RestaurentTracker import Restaurent_tracker
from Config import get_db
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=RestaurantResponse)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    try:
        # normalized_name = data.name.strip().lower()
        # restaurant = db.query(Restaurant).filter(
        #     func.lower(Restaurant.name) == normalized_name
        # ).first()

        # if restaurant:
        #     raise HTTPException(status_code=409, detail="Restaurant Already Exists")
        
        new_restaurant = Restaurant(**data.dict())
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)


        restaurant_log = Restaurent_tracker(
                restaurant_id=new_restaurant.id,
                is_online=1,
                online_time=datetime.utcnow()
            )
        
        db.add(restaurant_log)
        db.commit()

        return new_restaurant  # Return the created restaurant, matching the response_model

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
