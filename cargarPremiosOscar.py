import os
import requests
from pymongo import MongoClient

api_url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"

mongo_uri = os.getenv("MONGO_URI")

def fetch_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return None

def upload_to_mongo(data):
    client = MongoClient(mongo_uri)
    db = client["oscar_db"]
    collection = db["PremiosOscar"]

    if not data or "nominations" not in data:
        print("Datos no válidos o incompletos.")
        return

    for item in data["nominations"]:
        category = item.get("category")
        year = item.get("year")
        nominees = item.get("nominees", [])
        movies = item.get("movies", [])

        for nominee, movie in zip(nominees, movies):
            title = movie.get("title")

            document = {"category": category, "year": year, "nominee": nominee}
            if nominee != title:
                document["title"] = title

            collection.update_one({"category": category, "year": year, "nominee": nominee}, {"$set": document}, upsert=True)

    print("Datos cargados exitosamente a MongoDB.")

def main():
    data = fetch_data()
    if data:
        upload_to_mongo(data)

if __name__ == "__main__":
    main()

