import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri)
    print("Conexión exitosa a MongoDB Atlas.")
except Exception as e:
    print("Error al conectarse a MongoDB Atlas:", e)
    exit()

def cargarPremiosOscar():
    url = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        db = client["PremiosOscarDB"]
        collection = db["Winners"]

        for item in data:
            if item.get('won') and item.get('movies'):
                year = item.get('year', '')
                category = item.get('category', '')
                nominees = item.get('nominees', [None])
                movie = item['movies'][0]
                movie_title = movie.get('title', '')

                nominee_to_store = nominees[0] if nominees[0] != movie_title else None

                document = {
                    "year": year,
                    "category": category,
                    "movie_title": movie_title,
                }

                if nominee_to_store:
                    document["nominee"] = nominee_to_store

                if not collection.find_one(document):
                    collection.insert_one(document)
                else:
                    print(f"El documento ya existe: {document}")

        print("Los datos de los Premios Oscar se han cargado en MongoDB.")
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")

cargarPremiosOscar()
