import sys
import os

# Allow import from root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 404  # No root route

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    new_sheep = {
        "id": 7,
        "name": "Suffie",
        "breed": "Suffolk",
        "sex": "ram"
    }
    response = client.post("/sheep", json=new_sheep)
    assert response.status_code == 201
    assert response.json() == new_sheep

    get_response = client.get("/sheep/7")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep

def test_update_sheep():
    updated = {
        "id": 1,
        "name": "Spicey",
        "breed": "Gotland",
        "sex": "ewe"
    }
    response = client.put("/sheep/1", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "Spicey"

def test_delete_sheep():
    response = client.delete("/sheep/6")
    assert response.status_code == 200
    assert response.json()["name"] == "Esther"

    check = client.get("/sheep/6")
    assert check.status_code == 404

def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(s["name"] == "Spicey" for s in response.json())
