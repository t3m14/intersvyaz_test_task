from pydantic import BaseModel, Field
from typing import Optional

class Step(BaseModel):
    id: Optional[int] = None
    name: str 
    order: int
