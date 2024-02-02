from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.database import Base

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

class Auto(Base):
    id = Column(Integer, primary_key=True)
    is_detected = Column(Boolean)
    x_coord = Column(Integer, nullable=True)
    y_coord = Column(Integer, nullable=True)
    w = Column(Integer, nullable=True)
    h = Column(Integer, nullable=True)
    