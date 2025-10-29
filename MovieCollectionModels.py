from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field
from MovieCollectionDatabase import Base

# SQLAlchemy Model
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    director = Column(String)

# Pydantic Schemas
class MovieCreate(BaseModel):
    title: str = Field(..., min_length=1)
    year: int = Field(..., ge=1888, le=2100)
    director: str

class MovieOut(MovieCreate):
    id: int
    class Config:
        orm_mode = True
