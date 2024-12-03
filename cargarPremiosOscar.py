import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

api_url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    nominations = data.get("nominations", {})
else:
    print(f"Error al obtener datos de la API: {response.status_code}")
    exit()

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://dblanco:XPi8dTIHmjuk9bH9@cluster0.elpgy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(mongo_uri)
db = client["PremiosOscar"]
collection = db["Nominaciones"]

for category_data in nominations.get("categories", []):
    category_name = category_data.get("name")
    year = nominations.get("year")
    nominees = category_data.get("nominees", [])

    for nominee in nominees:
        document = {
            "category": category_name,
            "year": year,
            "nominee": nominee,
        }
        
        if not collection.find_one(document):
            collection.insert_one(document)

print("Datos cargados correctamente en MongoDB.")
