from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Pipeline(Base):
    __tablename__ = 'pipelines'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    steps = relationship("PipelineStep", back_populates="pipeline")

class PipelineStep(Base):
    __tablename__ = 'pipeline_steps'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    order = Column(Integer)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    pipeline = relationship("Pipeline", back_populates="steps")
