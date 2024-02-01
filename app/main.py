from fastapi import FastAPI, Depends, status, HTTPException
from app.database.piplines import get_piplines_list, get_pipeline_steps, get_pipeline, create_pipeline, edit_pipeline, delete_pipeline
from app.database.pipline_steps import get_steps_list_by_pipeline, get_step, create_step, edit_step, delete_step
from app.database.database import SessionLocal, Base, engine
from app.schemas.pipline_schema import Pipline
from app.schemas.pipline_step_schema import Step
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# CRUD for pipline
@app.get("/piplines")
async def get_piplines_route(db: Session = Depends(get_db), status_code=201) -> list[Pipline]:
    res = get_piplines_list(db)
    if res == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
@app.get("/piplines/{pipeline_id}")
async def get_pipeline_by_id_route(pipeline_id: int, db: Session = Depends(get_db), response_model=Pipline, status_code=status.HTTP_200_OK):
        res = get_pipeline(pipeline_id, db)
        if res is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return res
@app.post("/piplines")
async def create_pipeline_route(pipline: Pipline, db: Session = Depends(get_db), status_code=201) -> Pipline:
    return create_pipeline(pipline.name, db)

@app.put("/piplines/{pipeline_id}", status_code=status.HTTP_200_OK)
async def edit_pipeline_route(pipeline_id: int, pipline: Pipline, db: Session = Depends(get_db)):
    res = edit_pipeline(pipeline_id, pipline.name, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
@app.delete("/piplines/{pipeline_id}")
async def delete_pipeline_route(pipeline_id: int, pipline: Pipline, db: Session = Depends(get_db)):
    res = delete_pipeline(pipeline_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
    
# CRUD for pipline steps
@app.get("/piplines/{pipeline_id}/steps")
async def get_steps_by_pipeline_route(pipeline_id: int, db: Session = Depends(get_db)) -> list[Step]:
    res = get_steps_list_by_pipeline(pipeline_id, db)
    if res == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
@app.get("/piplines/{pipeline_id}/steps/{step_id}")
async def get_step_by_id_route(pipeline_id: int, step_id: int, step: Step, db: Session = Depends(get_db)):
    res = get_step(step_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res

@app.post("/piplines/{pipeline_id}/steps")
async def create_step_route(pipeline_id: int, step: Step, db: Session = Depends(get_db)):
    return create_step(step.name, step.order, pipeline_id, db)

@app.put("/piplines/{pipeline_id}/steps/{step_id}")
async def edit_step_route(pipeline_id: int, step_id: int, name: str, order: int, step: Step, db: Session = Depends(get_db)):
    res = edit_step(step_id, name, order, pipeline_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
    
@app.delete("/piplines/{pipeline_id}/steps/{step_id}")
async def delete_step_route(pipeline_id: int, step_id: int, step: Step, db: Session = Depends(get_db)):
    res = delete_step(step_id, db)
    
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res

