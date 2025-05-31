from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Config import get_db
from Models.RestaurentModel import Restaurant
from Models.RestaurentTracker import Restaurent_tracker
from datetime import datetime

router = APIRouter()
@router.patch("/{restaurant_id}/status/{status}")
def update_status(restaurant_id: int, status: int, db: Session = Depends(get_db)):
    try:
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        restaurant.status = status
        db.commit()
        db.refresh(restaurant)

        if status == 1:
            restaurant_log = Restaurent_tracker(
                restaurant_id=restaurant.id,
                is_online=1,
                online_time=datetime.utcnow()
            )
            db.add(restaurant_log)
            db.commit()
            db.refresh(restaurant_log)
            return {"status": "active"}

        elif status == 0:
            last_log = (
                db.query(Restaurent_tracker)
                .filter(
                    Restaurent_tracker.restaurant_id == restaurant_id,
                    Restaurent_tracker.is_online == 1,
                    Restaurent_tracker.offline_time.is_(None)
                )
                .order_by(Restaurent_tracker.online_time.desc())
                .first()
            )
            if last_log:
                last_log.offline_time = datetime.utcnow()
                last_log.is_online = status
                db.add(last_log)
                db.commit()
                db.refresh(last_log)
                return {"status": "inactive"}
            else:
                raise HTTPException(status_code=400, detail="No active online session found to close.")
        
        else:
            raise HTTPException(status_code=400, detail="Invalid status value")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
