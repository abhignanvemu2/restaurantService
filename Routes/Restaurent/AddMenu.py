# Routers/Menu.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config import get_db
from Models.MenuItem import MenuItem
from Models.RestaurentModel import Restaurant
from Schemas.MenuItem import MenuItemCreate

router = APIRouter()

@router.post("/{restaurant_id}/menu")
def create_menu_item(
    restaurant_id: int,
    item: MenuItemCreate,
    db: Session = Depends(get_db)
):
    try:
        # ✅ Check if the restaurant exists
        restaurant = db.query(Restaurant).filter_by(id=restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail=f"Restaurant with id {restaurant_id} does not exist")

        # ✅ Add new menu item
        new_item = MenuItem(
            restaurant_id=restaurant_id,
            name=item.name,
            description=item.description,
            price=item.price,
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return {
            "message": "Menu item added successfully",
            "menu_item": {
                "id": new_item.id,
                "name": new_item.name,
                "description": new_item.description,
                "price": new_item.price,
                "available": "active" if new_item.available == 1 else "inActive"
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating menu item: {str(e)}")
