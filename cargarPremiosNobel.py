import os
import requests
from pymongo import MongoClient
from io import StringIO
import csv
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()
uri = os.getenv("MONGO_URI")

# Conexión a MongoDB Atlas
try:
    client = MongoClient(uri)
    print("Conexión exitosa a MongoDB Atlas.")
except Exception as e:
    print("Error al conectarse a MongoDB Atlas:", e)
    exit()

def cargarPremiosNobel():
    # URL de la API del Premio Nobel
    url = "http://api.nobelprize.org/v1/prize.csv"
    
    # Realizar la solicitud GET
    response = requests.get(url)
    
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        
        # Conexión a la base de datos y colección
        db = client["PremiosPrizes"]
        collection = db["NobelWinners"]

        # Insertar datos en la colección
        for row in reader:
            # Obtener los datos relevantes del archivo CSV
            year = row['year']
            category = row['category']
            nobel_id = row['id']
            firstname = row.get('firstname', '').strip()
            surname = row.get('surname', '').strip()
            motivation = row.get('motivation', '').replace('"""', '').strip()
            share = row['share']
            
            # Documento a insertar
            document = {
                "year": year,
                "category": category,
                "id": nobel_id,
                "firstname": firstname,
                "surname": surname,
                "motivation": motivation,
                "share": share
            }
            
            # Insertar el documento si no existe
            if not collection.find_one({"year": year, "category": category, "id": nobel_id}):
                collection.insert_one(document)
            else:
                print(f"El documento ya existe: {document}")

        print("Los datos de los Premios Nobel se han cargado en MongoDB Atlas.")
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")

# Llamar a la función para cargar los Premios Nobel
cargarPremiosNobel()
