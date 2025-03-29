from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep

app = FastAPI()

@app.get("/sheep", response_model=list[Sheep])
def read_all_sheep():
    return list(db.data.values())

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep:
        return sheep
    raise HTTPException(status_code=404, detail="Sheep not found")

@app.post("/sheep", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    try:
        return db.add_sheep(sheep)
    except ValueError:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, updated_sheep: Sheep):
    try:
        return db.update_sheep(id, updated_sheep)
    except ValueError:
        raise HTTPException(status_code=404, detail="Sheep not found")

@app.delete("/sheep/{id}", response_model=Sheep)
def delete_sheep(id: int):
    try:
        return db.delete_sheep(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Sheep not found")
