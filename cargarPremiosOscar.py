import os
import requests
from pymongo import MongoClient

api_url = "http://127.0.0.1:8000/winners/"

mongo_uri = os.getenv("MONGO_URI")

response = requests.get(api_url)
data = response.json()["winners"]

client = MongoClient(mongo_uri)
db = client["PremiosOscar"]
collection = db["Ganadores"]

for entry in data:
    category = entry["category"]
    year = entry["year"]
    nominees = entry["nominees"]
    movies = entry["movies"]
    
    for movie in movies:
        title = movie["title"]
        
        if title in nominees:
            nominee_str = title
            document = {
                "category": category,
                "year": year,
                "nominee": nominee_str,
            }
        else:
            nominee_str = ", ".join(nominees)
            document = {
                "category": category,
                "year": year,
                "nominee": nominee_str,
                "title": title,
            }

        if not collection.find_one({"title": title, "nominee": nominee_str}):
            collection.insert_one(document)

print("Datos cargados correctamente en MongoDB.")
