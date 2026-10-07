import pytest

from app import create_app
from app.inventory import inventory


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    inventory.clear()
    inventory.append({
        "id": 1,
        "product_name": "Milk",
        "brands": "Test Brand",
        "price": 100,
        "stock": 10,
        "barcode": "123456",
        "ingredients_text": "Milk"
    })

    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.json["product_name"] == "Milk"


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404


def test_create_item(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Bread",
            "brands": "Test Bread",
            "price": 150,
            "stock": 20,
            "barcode": "789012"
        }
    )

    assert response.status_code == 201
    assert response.json["product_name"] == "Bread"


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 120,
            "stock": 15
        }
    )

    assert response.status_code == 200
    assert response.json["price"] == 120
    assert response.json["stock"] == 15


def test_delete_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200

    response = client.get("/inventory/1")
    assert response.status_code == 404


def test_create_item_missing_fields(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Incomplete Product"
        }
    )

    assert response.status_code == 400