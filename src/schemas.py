from datetime import date
from typing import List, Union

from pydantic import BaseModel, Field, Json


class PointData(BaseModel):
    date: date
    value: float


class DataWithType(BaseModel):
    x_data_type: str
    y_data_type: str
    x: List[PointData]
    y: List[PointData]


class HealthData(BaseModel):
    user_id: int
    data: DataWithType


class PearsonCorrelation(BaseModel):
    value: float
    p_value: float


class CorrelationSchema(BaseModel):
    user_id: int
    x_data_type: str
    y_data_type: str
    correlation: Union[Json, PearsonCorrelation]

    class Config:
        orm_mode = True


class CalculateCreateResponse(BaseModel):
    message: str = Field(example="Task sent in the background")


class CorrelationWrongResponse(BaseModel):
    detail: str = Field(example="Such data doesnt exist")
