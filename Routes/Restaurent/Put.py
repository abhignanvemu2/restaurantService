from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Models.RestaurentModel import Restaurant
from Schemas.Restaurent import UpdateRestaurant, RestaurantResponse
from Config import get_db

router = APIRouter()

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: int, data: UpdateRestaurant, db: Session = Depends(get_db)):
    try:
        # Find the restaurant by ID
        restaurant = db.get(Restaurant, restaurant_id)

        # If the restaurant doesn't exist, raise an error
        if restaurant is None:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Update the restaurant's fields
        restaurant.name = data.name
        # restaurant.status = data.status
        restaurant.description = data.description

        # Commit the changes
        db.commit()

        # Refresh the restaurant to get the updated data
        db.refresh(restaurant)

        return restaurant
    
    except SQLAlchemyError as e:
        # If any SQL error occurs, raise an HTTPException with a 500 status code
        db.rollback()  # Rollback in case of error to avoid uncommitted changes
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    except Exception as e:
        # Catch other unexpected exceptions and raise a 500 error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
