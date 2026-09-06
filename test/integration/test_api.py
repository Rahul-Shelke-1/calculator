import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_calculate_addition(client):
    response = client.post("/math", json={"operation": "add", "num1": 2, "num2": 3})

    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_calculate_subtraction(client):
    response = client.post("/math", json={"operation": "subtract", "num1": 5, "num2": 2})

    assert response.status_code == 200
    assert response.get_json()["result"] == 3


def test_calculate_multiplication(client):
    response = client.post("/math", json={"operation": "multiply", "num1": 2, "num2": 4})

    assert response.status_code == 200
    assert response.get_json()["result"] == 8


def test_calculate_division(client):
    response = client.post("/math", json={"operation": "divide", "num1": 10, "num2": 2})

    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_calculate_division_by_zero(client):
    response = client.post("/math", json={"operation": "divide", "num1": 10, "num2": 0})    

    assert response.status_code == 500
