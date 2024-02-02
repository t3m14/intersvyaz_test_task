from fastapi import FastAPI, Depends, status, HTTPException, File
from app.database.piplines import get_piplines_list, get_pipeline_steps, get_pipeline, create_pipeline, edit_pipeline, delete_pipeline
from app.database.pipline_steps import get_steps_list_by_pipeline, get_step, create_step, edit_step, delete_step
from app.database.database import SessionLocal, Base, engine
from app.schemas.pipline_schema import Pipline
from app.schemas.pipline_step_schema import Step
from sqlalchemy.orm import Session
from typing import Annotated


from app.tasks.tasks import *

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()



app = FastAPI()

@app.post("/process_image")
async def process_image(image: Annotated[bytes, File(description="A file read as bytes")], pipeline_id: int, db: Session = Depends(get_db)):
    
    steps = get_steps_list_by_pipeline(pipeline_id, db)
    processed_image, detected_box = None, None
    for step in step:
        # Подумать над тем, как избежать бесконечные if step == stepname
        
        if step == 'resize_and_convert_to_base64':
            # Обработка изображения
            processed_image = await resize_and_convert_to_base64.delay(image, pipeline_id)
        if step == 'run_ml_model':
            # Прогон обработанного изображения через модель машинного обучения
            detected_box = await run_ml_model.delay(processed_image)
        if step =='save_to_db':
            # Сохранение в БД информации
            await save_to_db.delay(detected_box)

    return {"message": "Image processed successfully"}
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
async def delete_pipeline_route(pipeline_id: int, db: Session = Depends(get_db)):
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
async def get_step_by_id_route(pipeline_id: int, step_id: int, db: Session = Depends(get_db)):
    res = get_step(step_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res

@app.post("/piplines/{pipeline_id}/steps")
async def create_step_route(pipeline_id: int, step: Step, db: Session = Depends(get_db)):
    return create_step(step.name, step.order, pipeline_id, db)

@app.put("/piplines/{pipeline_id}/steps/{step_id}")
async def edit_step_route(pipeline_id: int, step_id: int, step: Step, db: Session = Depends(get_db)):
    res = edit_step(step_id, step.name, step.order, pipeline_id, db)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res
    
@app.delete("/piplines/{pipeline_id}/steps/{step_id}")
async def delete_step_route(pipeline_id: int, step_id: int, db: Session = Depends(get_db)):
    res = delete_step(step_id, db)
    
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return res

