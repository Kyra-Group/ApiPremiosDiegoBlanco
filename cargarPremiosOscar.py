import requests
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"
response = requests.get(url)
data = response.json()['nominations']

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client['PremiosOscar']
collection = db['Ganadores']

for nomination in data:
    # Verificar si el premio fue ganado
    if not nomination['won']:
        continue

    category = nomination['category']
    year = nomination['year']
    nominees = nomination['nominees']
    movies = nomination['movies']

    movie_titles = []
    for movie in movies:
        title = movie['title']
        
        # Si el título de la película está en los nominados, lo añadimos solo a los nominados.
        if title in nominees:
            nominees = [title]
        else:
            movie_titles.append(title)  # Si no coincide, lo añadimos a movie_titles
    
    if len(nominees) == 1:
        nominees = nominees[0]  # Si hay solo un nominado, asignamos directamente

    # Preparar el documento para MongoDB
    document = {
        "category": category,
        "year": year,
        "nominees": nominees
    }

    # Si tenemos títulos adicionales que no son nominados, los agregamos a "title"
    if movie_titles:
        document["title"] = movie_titles

    # Insertar el documento en la colección
    collection.insert_one(document)
