from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config import get_db
from Models.MenuItem import MenuItem
from Schemas.MenuItem import MenuItemUpdate

router = APIRouter()

@router.patch("/menu/{item_id}")
def update_menu_item(
    item_id: int,
    updated_fields: MenuItemUpdate,
    db: Session = Depends(get_db)
):
    try:
        item = db.query(MenuItem).filter_by(id=item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Menu item with id {item_id} not found")

        # Only update fields that are provided
        if updated_fields.name is not None:
            item.name = updated_fields.name
        if updated_fields.description is not None:
            item.description = updated_fields.description
        if updated_fields.price is not None:
            item.price = updated_fields.price
        if updated_fields.available is not None:
            item.available = updated_fields.available

        db.commit()
        db.refresh(item)

        return {
            "message": "Menu item updated successfully",
            "menu_item": {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "available": "active" if item.available == 1 else "inActive"
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating menu item: {str(e)}")
