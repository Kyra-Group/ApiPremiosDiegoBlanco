import requests
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client["PremiosOscar"] 
collection = db["Ganadores"]

url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    nominations_won = [nom for nom in data["nominations"] if nom["won"]]

    filtered_data = []
    for nom in nominations_won:
        for movie in nom["movies"]:
            # Si 'nominees' tiene solo un elemento, lo convertimos en un string
            nominees = nom["nominees"][0] if len(nom["nominees"]) == 1 else nom["nominees"]
            
            filtered_data.append({
                "category": nom["category"],
                "year": nom["year"],
                "nominees": nominees,
                "title": movie["title"]
            })

    if filtered_data:
        collection.insert_many(filtered_data)
        print(f"Se han insertado {len(filtered_data)} documentos en MongoDB.")
    else:
        print("No se encontraron nominaciones con 'won' = true.")
else:
    print(f"Error al obtener los datos de la API: {response.status_code}")
