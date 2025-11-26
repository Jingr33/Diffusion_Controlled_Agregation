from sqlalchemy import Column, Integer, Float

from database.models.base import Base

class GyrationRatio(Base):
    __tablename__ = 'gyration_ratio'
    id = Column(Integer, primary_key = True)
    atoms = Column(Integer, nullable = False)
    cube_gr = Column(Float, nullable = True)
    sphere_gr = Column(Float, nullable = True)
    random_gr = Column(Float, nullable = True)
