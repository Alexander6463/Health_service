from sqlalchemy import Column, Float, Integer, String

from db.base import Base


class Correlation(Base):
    __tablename__ = "Correlation"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    x_data_type = Column(String(50), nullable=False)
    y_data_type = Column(String(50), nullable=False)
    correlation = Column(String(100), nullable=False)
