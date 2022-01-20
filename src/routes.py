import logging
from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.base import get_db
from db.models import Correlation
from src.auth import create_access_token
from src.schemas import (CalculateCreateResponse, CorrelationSchema,
                         CorrelationWrongResponse, HealthData)
from src.utils import calculate

router = APIRouter()
auth_router = APIRouter()

LOGGER = logging.getLogger(__file__)

security = HTTPBearer()


@router.post(
    "/calculate",
    responses={
        200: {
            "model": CalculateCreateResponse,
            "description": "Successfully created",
        }
    },
)
def calculate_data(
    request: HealthData,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db),
):
    background_tasks.add_task(calculate, request=request, session=session)
    LOGGER.info("Add background task with params %s", request)
    return {"message": "Task sent in the background"}


@router.get(
    "/correlation",
    response_model=CorrelationSchema,
    responses={
        200: {
            "model": CorrelationSchema,
            "description": "Successful",
        },
        404: {
            "model": CorrelationWrongResponse,
            "description": "Such data doesnt exist",
        },
    },
)
def get_correlation_data(
    x_data_type: str, y_data_type: str, user_id: int, session: Session = Depends(get_db)
):
    correlation_data = (
        session.query(Correlation)
        .filter(
            and_(
                Correlation.user_id == user_id,
                Correlation.x_data_type == x_data_type,
                Correlation.y_data_type == y_data_type,
            )
        )
        .first()
    )
    if correlation_data:
        return CorrelationSchema.from_orm(correlation_data)

    LOGGER.info("Such data doesnt exist")
    raise HTTPException(
        status_code=404,
        detail="Such data doesnt exist",
    )


@auth_router.get("/token")
def get_token(expires_delta: timedelta = None):
    return create_access_token(expires_delta=expires_delta)
