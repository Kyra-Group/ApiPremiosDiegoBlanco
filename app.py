from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGO_URI")

client = MongoClient(uri)
db = client["PremiosOscarDB"]
collection = db["Winners"]

app = FastAPI()
def serialize_document(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/")
def root():
    return {"message": "API de Premios Oscar"}

@app.get("/winners")
def get_all_winners():
    winners = list(collection.find())
    return {"data": [serialize_document(w) for w in winners]}

@app.get("/winners/{year}")
def get_winners_by_year(year: int):
    winners = list(collection.find({"year": year}))
    if not winners:
        raise HTTPException(status_code=404, detail="No se encontraron ganadores para este año")
    return {"data": [serialize_document(w) for w in winners]}

@app.post("/winners")
def add_winner(winner: dict):
    result = collection.insert_one(winner)
    return {"message": "Ganador añadido", "id": str(result.inserted_id)}

@app.delete("/winners/{winner_id}")
def delete_winner(winner_id: str):
    result = collection.delete_one({"_id": ObjectId(winner_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ganador no encontrado")
    return {"message": "Ganador eliminado"}
