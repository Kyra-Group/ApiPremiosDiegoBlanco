import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import urllib3  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
uri = os.getenv("MONGO_URI")

# Configuración de MongoDB
try:
    client = MongoClient(uri)
    db = client["PremioCervantesDB"]
    collection = db["Winners"]
    print("Conexión exitosa a MongoDB.")
except Exception as e:
    print(f"Error al conectarse a MongoDB: {e}")
    exit()

def cargar_premio_cervantes():
    url = "https://www.cultura.gob.es/premiado/busquedaPremioParticularAction.do?action=busquedaInicial&params.id_tipo_premio=90&layout=premioMiguelCervantesLibro&cache=init&language=es"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        lista_premiados = soup.find('div', class_='listaPremiados')
        
        if lista_premiados:
            premiados = lista_premiados.find_all('li')

            for premiado in premiados:
                year = premiado.text.split('-')[0].strip()
                name_tag = premiado.find('a', class_='titulo')
                
                if name_tag:
                    name = name_tag.text.strip()
                    link = "https://www.cultura.gob.es" + name_tag['href']

                    document = {
                        "year": year,
                        "name": name,
                        "link": link
                    }

                    if not collection.find_one({"year": year, "name": name}):
                        collection.insert_one(document)
                    else:
                        print(f"El documento para el año {year} y el premiado {name} ya existe.")
            
            print("Los datos del Premio Cervantes se han cargado a MongoDB.")
        else:
            print("No se encontró la lista de premiados.")
    else:
        print(f"Error al acceder a la página: {response.status_code}")

cargar_premio_cervantes()
