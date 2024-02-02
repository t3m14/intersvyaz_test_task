from sqlalchemy.orm import Session
from app.database.models import Auto
def create_auto(is_detected: str, x_coord: int | None, y_coord: int | None, w: int | None, h: int | None, db: Session) -> Auto:
    db_auto = Auto(is_detected=is_detected, x_coord=x_coord, y_coord=y_coord, w=w, h=h)
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto