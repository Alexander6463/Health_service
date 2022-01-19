import json
import logging

import numpy as np
from scipy import stats
from sqlalchemy import and_
from sqlalchemy.orm import Session

from db.models import Correlation
from src.schemas import HealthData

LOGGER = logging.getLogger(__file__)


def delete_not_pair_dates(health_obj: HealthData) -> HealthData:
    """Create new list of x and y with pair dates"""

    set_date_x = set()
    data_y = sorted(health_obj.data.y, key=lambda x: x.date)
    data_x = sorted(health_obj.data.x, key=lambda x: x.date)
    health_obj.data.y = []
    health_obj.data.x = []
    for element in data_x:
        set_date_x.add(element.date)

    for element in data_y:
        if element.date in set_date_x:
            health_obj.data.y.append(element)
            set_date_x.remove(element.date)

    for element in data_x:
        if element.date not in set_date_x:
            health_obj.data.x.append(element)
    return health_obj


def calculate_pearson_coefficient(health_obj: HealthData):
    """Calculate pearson coefficient and p value"""

    health_obj = delete_not_pair_dates(health_obj)
    data_x, data_y = [], []
    for el_x, el_y in zip(health_obj.data.x, health_obj.data.y):
        data_x.append(el_x.value)
        data_y.append(el_y.value)
    correlation = np.nan_to_num(stats.pearsonr(x=data_x, y=data_y))
    return json.dumps({"value": correlation[0], "p_value": correlation[1]})


def calculate(request: HealthData, session: Session) -> None:
    """Select from database record with user_id, x_data_type, y_data_type
    and if such object exists then update it. In other way create new record."""
    LOGGER.info(
        "Start calculate pearson coefficient with x: %s, y: %s, user: %s",
        request.data.x_data_type,
        request.data.y_data_type,
        request.user_id,
    )
    data = (
        session.query(Correlation)
        .filter(
            and_(
                Correlation.user_id == request.user_id,
                Correlation.x_data_type == request.data.x_data_type,
                Correlation.y_data_type == request.data.y_data_type,
            )
        )
        .first()
    )
    if not data:
        correlation_data = Correlation(
            user_id=request.user_id,
            x_data_type=request.data.x_data_type,
            y_data_type=request.data.y_data_type,
            correlation=calculate_pearson_coefficient(request),
        )
        session.add(correlation_data)
        session.commit()
    else:
        data.correlation = calculate_pearson_coefficient(request)
        session.commit()
