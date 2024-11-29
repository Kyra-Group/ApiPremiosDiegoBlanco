from fastapi import FastAPI
from pymongo import MongoClient
import os
from pydantic import BaseModel

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["oscar_nominations"]
collection = db["winners"]

app = FastAPI()

class Nominee(BaseModel):
    year: str
    category: str
    movie_title: str
    nominee: str = None

@app.post("/winners")
def create_winner(nominee: Nominee):
    document = nominee.dict()
    result = collection.insert_one(document)
    if result.inserted_id:
        return {"message": "Winner added successfully"}
    else:
        return {"message": "Failed to add winner"}
