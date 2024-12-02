import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# Crear una instancia de FastAPI
app = FastAPI()

# URL de la API original
url = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

# Obtener los datos de la API
response = requests.get(url)
data = response.json()

# Definir modelos Pydantic para la validación y estructuración de datos
class Movie(BaseModel):
    title: str
    tmdb_id: int
    imdb_id: str

class Nomination(BaseModel):
    category: str
    year: str
    nominees: List[str]
    title: str = None

# Filtrar los datos según las condiciones solicitadas
filtered_data = []

for item in data:
    category = item['category']
    year = item['year']
    nominees = item['nominees']
    movies = item['movies']
    
    # Si nominees y title son iguales, solo se guarda nominees
    if nominees == [movie['title'] for movie in movies]:
        filtered_data.append({
            'category': category,
            'year': year,
            'nominees': nominees
        })
    else:
        for movie in movies:
            filtered_data.append({
                'category': category,
                'year': year,
                'nominees': nominees,
                'title': movie['title']
            })

# Ruta para la nueva API que retorna los datos filtrados
@app.get("/api/oscarnominations")
def get_nominations():
    return filtered_data
