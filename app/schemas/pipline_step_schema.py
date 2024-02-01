from pydantic import BaseModel, Field

class Step(BaseModel):
    id: int|None = Field(auto_increment=True, pk_field=True, alias='_id')
    name: str
    order: int
    pipeline_id: int