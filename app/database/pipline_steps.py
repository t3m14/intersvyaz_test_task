from sqlalchemy.orm import Session
from app.database.models import Pipeline, PipelineStep

def get_steps_list_by_pipeline(pipeline_id: int, db: Session) -> list[PipelineStep]:
    return db.query(PipelineStep).filter(PipelineStep.pipeline_id == pipeline_id).all()

def get_step(step_id: int, db: Session) -> PipelineStep:
    return db.query(PipelineStep).filter(PipelineStep.id == step_id).first()

def create_step(name: str, order: int, pipeline_id: int, db: Session) -> PipelineStep:
    db_step = PipelineStep(name=name, order=order, pipeline_id=pipeline_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

def edit_step(step_id: int, name: str, order: int, pipeline_id: int, db: Session) -> Pipeline:
    db_step = get_step(step_id, db)
    if db_step is None:
        return None
    db_step.name = name
    db_step.order = order
    db_step.pipeline_id = pipeline_id
    db.commit()
    db.refresh(db_step)
    return db_step
def delete_step(step_id: int, db: Session) -> Pipeline:
    db_step = get_step(step_id, db)
    if db_step is None:
        return None
    db.delete(db_step)
    db.commit()
    return db_step
