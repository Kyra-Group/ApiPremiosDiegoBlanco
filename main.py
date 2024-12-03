from fastapi import FastAPI
import requests
import json

# Crear una instancia de FastAPI
app = FastAPI()

# URL del archivo JSON
json_url = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

# Descargar el archivo JSON
def fetch_json():
    response = requests.get(json_url)
    response.raise_for_status()  # Verificar errores
    return response.json()

# Almacenar los datos del JSON en memoria
data = fetch_json()

# Crear un endpoint para acceder al contenido del JSON
@app.get("/api/nominations")
def get_nominations():
    return {"nominations": data}

# Mensaje inicial
@app.get("/")
def read_root():
    return {"message": "API de Nominaciones al Oscar. Visita /api/nominations para ver los datos."}
