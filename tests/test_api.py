import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import Base, get_db
from main import app
from src.schemas import CorrelationSchema, DataWithType, HealthData, PointData

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_calculate():
    data = HealthData(
        user_id=1,
        data=DataWithType(
            x_data_type="test_x",
            y_data_type="test_y",
            x=[
                PointData(date="2021-01-01", value=1),
                PointData(date="2021-01-02", value=2),
                PointData(date="2021-01-03", value=3),
            ],
            y=[
                PointData(date="2021-01-01", value=2.0),
                PointData(date="2021-01-02", value=4.0),
                PointData(date="2021-01-03", value=6.0),
            ],
        ),
    )
    response = client.post("/calculate", data=data.json())
    assert response.status_code == 200
    assert response.content == b'{"message":"Task sent in the background"}'


def test_create_calculate_with_bad_data():
    data = HealthData(
        user_id=2,
        data=DataWithType(
            x_data_type="test_x",
            y_data_type="test_y",
            x=[
                PointData(date="2021-01-01", value=1),
                PointData(date="2021-01-02", value=1),
                PointData(date="2021-01-03", value=1),
            ],
            y=[
                PointData(date="2021-01-01", value=2),
                PointData(date="2021-01-02", value=2),
                PointData(date="2021-01-03", value=2),
            ],
        ),
    )
    response = client.post("/calculate", data=data.json())
    assert response.status_code == 200
    assert response.content == b'{"message":"Task sent in the background"}'


def test_get_calculate():
    response = client.get(
        "/correlation?user_id=1&&y_data_type=test_y&&x_data_type=test_x"
    )
    result = CorrelationSchema(**json.loads(response.text))
    assert response.status_code == 200
    assert result.user_id == 1
    assert result.y_data_type == "test_y"
    assert result.x_data_type == "test_x"
    assert round(result.correlation.value) == 1
    assert round(result.correlation.p_value * 10 ** 8, ndigits=2) == 1.34


def test_get_calculate_with_pearson_null():
    response = client.get(
        "/correlation?user_id=2&&y_data_type=test_y&&x_data_type=test_x"
    )
    result = CorrelationSchema(**json.loads(response.text))
    assert response.status_code == 200
    assert result.user_id == 2
    assert result.y_data_type == "test_y"
    assert result.x_data_type == "test_x"
    assert result.correlation.value == 0
    assert result.correlation.p_value == 0
