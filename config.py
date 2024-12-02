import os

# Variable para verificar el entorno
IS_RENDER = os.getenv("RENDER") == "TRUE"

# URL de la API para los datos en Render
URL = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

def get_base_url():
    if IS_RENDER:
        # Devuelve la URL completa en Render si está en ese entorno
        return "https://your-app-name.onrender.com/winners/"
    else:
        # En desarrollo local, se usa la URL base de la app local
        return "http://127.0.0.1:8000/winners/"
