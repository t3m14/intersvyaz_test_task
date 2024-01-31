from fastapi import FastAPI
from database.piplines import get_piplines_list, get_pipeline_steps, get_pipeline, create_pipeline, edit_pipeline, delete_
from database.pipline_steps import get_steps_list_by_pipeline, get_step, create_step, edit_step, delete


app = FastAPI()

# CRUD for pipline
@app.get("/piplines")
async def get_piplines():
    return get_piplines_list()

@app.get("/piplines/{pipeline_id}")
async def get_pipeline_by_id(pipeline_id: int):
    return get_pipeline(pipeline_id)

@app.post("/piplines")
async def create_pipeline(name: str):
    return create_pipeline(name)

@app.put("/piplines/{pipeline_id}")
async def edit_pipeline(pipeline_id: int, name: str):
    return edit_pipeline(pipeline_id, name)

@app.delete("/piplines/{pipeline_id}")
async def delete_pipeline(pipeline_id: int):
    return delete_pipeline(pipeline_id)

# CRUD for pipline steps
@app.get("/piplines/{pipeline_id}/steps")
async def get_steps_by_pipeline(pipeline_id: int):
    return get_steps_list_by_pipeline(pipeline_id)

@app.get("/piplines/{pipeline_id}/steps/{step_id}")
async def get_step_by_id(pipeline_id: int, step_id: int):
    return get_step(step_id)

@app.post("/piplines/{pipeline_id}/steps")
async def create_step(pipeline_id: int, name: str, order: int):
    return create_step(name, order, pipeline_id)

@app.put("/piplines/{pipeline_id}/steps/{step_id}")
async def edit_step(pipeline_id: int, step_id: int, name: str, order: int):
    return edit_step(step_id, name, order, pipeline_id)

@app.delete("/piplines/{pipeline_id}/steps/{step_id}")
async def delete_step(pipeline_id: int, step_id: int):
    return delete_step(step_id)

