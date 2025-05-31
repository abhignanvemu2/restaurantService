from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Models.RestaurentModel import Restaurant
from Schemas.Restaurent import RestaurantResponse
from Config import get_db

router = APIRouter()

@router.get("/available", response_model=list[RestaurantResponse])
def get_available_restaurants(db: Session = Depends(get_db)):
    try:
        restaurants = db.query(Restaurant).filter(Restaurant.status == 1).all()
        if not restaurants:
            raise HTTPException(status_code=404, detail="No available restaurants found")

        return restaurants
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
