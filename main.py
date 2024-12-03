from fastapi import FastAPI
import requests
import json

# Crear una instancia de FastAPI
app = FastAPI()

# URL del archivo JSON
json_url = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

# Descargar el archivo JSON
def fetch_json():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(json_url, headers=headers)
    response.raise_for_status()  # Verificar errores
    return response.json()

# Almacenar los datos del JSON en memoria
try:
    data = fetch_json()
except requests.HTTPError as e:
    data = {"error": f"Failed to fetch data: {str(e)}"}

# Crear un endpoint para acceder al contenido del JSON
@app.get("/api/nominations")
def get_nominations():
    return {"nominations": data}

# Mensaje inicial
@app.get("/")
def read_root():
    return {"message": "API de Nominaciones al Oscar. Visita /api/nominations para ver los datos."}
