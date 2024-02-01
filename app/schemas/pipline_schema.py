from pydantic import BaseModel
from typing import Optional
from app.schemas.pipline_step_schema import Step

class Pipline(BaseModel):
    id: Optional[int] = None
    name: str
    steps: Optional[list[Step]] = None
