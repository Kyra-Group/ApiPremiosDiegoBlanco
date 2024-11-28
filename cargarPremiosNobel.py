import os
import requests
from pymongo import MongoClient
from io import StringIO
import csv
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri)
    print("Conexión exitosa a MongoDB Atlas.")
except Exception as e:
    print("Error al conectarse a MongoDB Atlas:", e)
    exit()

def cargarPremiosNobel():
    url = "http://api.nobelprize.org/v1/prize.csv"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        
        db = client["PremiosPrizes"]
        collection = db["NobelWinners"]

        for row in reader:
            year = row['year']
            category = row['category']
            nobel_id = row['id']
            firstname = row.get('firstname', '').strip()
            surname = row.get('surname', '').strip()
            motivation = row.get('motivation', '').replace('"""', '').strip()
            share = row['share']
            
            document = {
                "year": year,
                "category": category,
                "id": nobel_id,
                "firstname": firstname,
                "surname": surname,
                "motivation": motivation,
                "share": share
            }
            
            if not collection.find_one({"year": year, "category": category, "id": nobel_id}):
                collection.insert_one(document)
            else:
                print(f"El documento ya existe: {document}")

        print("Los datos de los Premios Nobel se han cargado en MongoDB Atlas.")
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")

cargarPremiosNobel()
