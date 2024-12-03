import os
import requests
from pymongo import MongoClient

# URL de la API
api_url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"

# URI de conexión a MongoDB
mongo_uri = os.getenv("MONGO_URI")

# Conectar a MongoDB Atlas
client = MongoClient(mongo_uri)
db = client['premios']  # Nombre de la base de datos
collection = db['nominations']  # Nombre de la colección

# Obtener datos de la API
response = requests.get(api_url)

# Verificar que la respuesta sea exitosa
if response.status_code == 200:
    data = response.json()

    # Filtrar solo los registros donde 'won' es True
    nominations = data.get("nominations", [])
    filtered_nominations = []

    for nomination in nominations:
        if nomination.get('won', False):
            # Preparamos el objeto a subir
            nominee_titles = nomination.get("nominees", [])
            movie_titles = [movie["title"] for movie in nomination.get("movies", [])]

            # Verificar si los 'nominees' y 'title' son iguales
            if sorted(nominee_titles) == sorted(movie_titles):
                # Solo subimos 'nominees' y 'title'
                filtered_nominations.append({
                    "category": nomination["category"],
                    "year": nomination["year"],
                    "nominees": nominee_titles,
                    "movies": [{"title": title} for title in nominee_titles]
                })
            else:
                # Subir todos los datos de 'nominees' y 'movies' como corresponda
                filtered_nominations.append({
                    "category": nomination["category"],
                    "year": nomination["year"],
                    "nominees": nominee_titles,
                    "movies": [{"title": movie["title"], "tmdb_id": movie["tmdb_id"], "imdb_id": movie["imdb_id"]} for movie in nomination.get("movies", [])]
                })

    # Insertar los registros filtrados en MongoDB
    if filtered_nominations:
        collection.insert_many(filtered_nominations)
        print("Datos subidos a MongoDB Atlas.")
    else:
        print("No hay datos para subir.")
else:
    print(f"Error al obtener los datos de la API. Código de estado: {response.status_code}")
