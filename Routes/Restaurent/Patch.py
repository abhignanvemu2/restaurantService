from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Models.RestaurentModel import Restaurant
from Schemas.Restaurent import UpdateStatus, RestaurantResponse
from Config import get_db

router = APIRouter()

@router.patch("/{restaurant_id}/status", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, data: UpdateStatus, db: Session = Depends(get_db)):
    try:
        # Find the restaurant by ID
        restaurant = db.get(Restaurant, restaurant_id)

        # If the restaurant doesn't exist, raise an error
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Update the restaurant's fields
        restaurant.status = data.status

        # Commit the changes
        db.commit()

        # Refresh the restaurant to get the updated data
        db.refresh(restaurant)

        return restaurant
    
    except SQLAlchemyError as e:
        
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
