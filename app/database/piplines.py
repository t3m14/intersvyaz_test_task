from sqlalchemy.orm import Session
from database.models import Pipeline, PipelineStep

def get_piplines_list(db: Session) -> list[Pipeline]:
    return db.query(Pipeline).all()

def get_pipeline_steps(pipeline_id: int, db: Session) -> list[PipelineStep]:
    return db.query(PipelineStep).filter(PipelineStep.pipeline_id == pipeline_id).all()

def get_pipeline(pipeline_id: int, db: Session) -> Pipeline:
    return db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
def create_pipeline(name: str, db: Session) -> Pipeline:
    db_pipeline = Pipeline(name=name)
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline
def edit_pipeline(pipeline_id: int, name: str, db: Session) -> Pipeline:
    db_pipeline = get_pipeline(pipeline_id, db)
    db_pipeline.name = name
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline
def delete_pipeline(pipeline_id: int, db: Session) -> Pipeline:
    db_pipeline = get_pipeline(pipeline_id, db)
    db.delete(db_pipeline)
    db.commit()
    return db_pipeline
