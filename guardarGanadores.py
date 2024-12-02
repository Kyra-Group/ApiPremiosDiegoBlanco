import requests
import json

LOCAL_URL = "https://nombre-de-tu-app.onrender.com/winners/"
LOCAL_FILE_PATH = "GanadoresOscar.json"

def fetch_winners_data():
    response = requests.get(LOCAL_URL)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener los datos del endpoint: {response.status_code}")

def save_data_to_file(data):
    with open(LOCAL_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Datos guardados exitosamente en {LOCAL_FILE_PATH}")

if __name__ == "__main__":
    try:
        data = fetch_winners_data()
        save_data_to_file(data)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
