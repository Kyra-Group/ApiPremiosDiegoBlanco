import os
import requests
from pymongo import MongoClient

# URL de la API
api_url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client['PremiosOScar'] 
collection = db['Ganadores']

response = requests.get(api_url)
data = response.json()
nominations_won = [
    nomination for nomination in data["nominations"] if nomination["won"]
]

for nomination in nominations_won:
    category = nomination["category"]
    year = nomination["year"]
    nominees = nomination["nominees"]
    
    # Filtrar títulos únicos de las películas
    movies = nomination["movies"]
    movie_titles = {movie["title"] for movie in movies}

    document = {
        "category": category,
        "year": year,
        "nominees": nominees,
        "movies": [{"title": title} for title in movie_titles]
    }

    collection.insert_one(document)

print("Datos subidos exitosamente a MongoDB Atlas.")
