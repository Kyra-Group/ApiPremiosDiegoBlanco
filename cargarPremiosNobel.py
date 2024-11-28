import requests
import csv
from io import StringIO
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv("MONGO_URI") 

try:
    client = MongoClient(uri)
    db = client["Winners"]
    collection = db["PremioNobelDB"]
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print(f"Error al conectarse a MongoDB: {e}")
    exit()

def cargar_premios_nobel():
    url = "http://api.nobelprize.org/v1/prize.csv"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)

        for row in reader:
            year = row['year']
            category = row['category']
            nobel_id = row['id']
            firstname = row['firstname']
            surname = row['surname']
            motivation = row['motivation'].replace('"""', '') if row['motivation'] else None
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
                print(f"El documento para el año {year}, categoría {category}, ID {nobel_id} ya existe.")

        print("Los datos de los Premios Nobel se han cargado a MongoDB.")
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")

cargar_premios_nobel()
