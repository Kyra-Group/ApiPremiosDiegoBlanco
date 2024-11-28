import os
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(uri)
    print("Conexión exitosa a MongoDB Atlas.")
except Exception as e:
    print("Error al conectarse a MongoDB Atlas:", e)
    exit()

def cargarBalonesDeOro():
    def obtener_datos_de_pagina(pagina_numero):
        base_url = f"https://www.transfermarkt.es/erfolge/spielertitel/statistik/676/page/{pagina_numero}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        
        response = requests.get(base_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error al acceder a la página {pagina_numero}: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        grid_view = soup.find('div', id='yw1', class_='grid-view')
        
        if not grid_view:
            print(f"No se encontró el div con id 'yw1' y clase 'grid-view' en la página {pagina_numero}.")
            return []
        
        return grid_view

    def obtener_nombre_imagen():
        datos_imagen_club = []
        
        for pagina_numero in range(1, 4):
            grid_view = obtener_datos_de_pagina(pagina_numero)
            
            tds_con_a = grid_view.find_all('td', class_='zentriert')
            
            for td in tds_con_a:
                a_tag = td.find('a')
                if a_tag:
                    nombre_club = a_tag.get('title')
                    img_tag = a_tag.find('img')
                    if img_tag:
                        imagen_url = img_tag.get('src')
                        datos_imagen_club.append({'club': nombre_club, 'imagen_url': imagen_url})
        
        return datos_imagen_club

    def obtener_año():
        años = []
        
        for pagina_numero in range(1, 4):
            grid_view = obtener_datos_de_pagina(pagina_numero)
            
            tds_con_año = grid_view.find_all('td', class_='zentriert hauptlink')
            
            for td in tds_con_año:
                año = td.text.strip()
                años.append(año)
        
        return años

    def obtener_nombre_imagen_jugador():
        jugadores_info = []
        
        for pagina_numero in range(1, 4):
            grid_view = obtener_datos_de_pagina(pagina_numero)
            
            tds_con_imagen_jugador = grid_view.find_all('td', class_='links no-border-rechts')
            
            for td in tds_con_imagen_jugador:
                a_tag = td.find('a', title=True)
                if a_tag:
                    nombre_jugador = a_tag.get('title')
                    img_tag = td.find('img')
                    if img_tag:
                        imagen_url = img_tag.get('src')
                        jugadores_info.append({'jugador': nombre_jugador, 'imagen_url': imagen_url})
        
        return jugadores_info

    def obtener_pais_imagen():
        paises_info = []
        
        for pagina_numero in range(1, 4):
            grid_view = obtener_datos_de_pagina(pagina_numero)
            
            tds_con_pais = grid_view.find_all('td', class_='zentriert')
            
            for td in tds_con_pais:
                img_tag = td.find('img', class_='flaggenrahmen')
                if img_tag:
                    pais_nombre = img_tag.get('title')
                    pais_imagen_url = img_tag.get('src')
                    paises_info.append({'pais': pais_nombre, 'imagen_url': pais_imagen_url})
        
        return paises_info

    datos_imagen_club = obtener_nombre_imagen()
    años = obtener_año()
    jugadores_info = obtener_nombre_imagen_jugador()
    paises_info = obtener_pais_imagen()
    
    if len(datos_imagen_club) != len(años) or len(datos_imagen_club) != len(jugadores_info) or len(datos_imagen_club) != len(paises_info):
        print("Los datos no tienen la misma longitud, hay un desajuste.")
        return

    # Conexión a MongoDB
    db = client["BalonDeOroDB"]
    collection = db["Winners"]

    for i in range(len(datos_imagen_club)):
        año = años[i]
        club = datos_imagen_club[i]['club']
        imagen_club_url = datos_imagen_club[i]['imagen_url']
        jugador = jugadores_info[i]['jugador']
        imagen_jugador_url = jugadores_info[i]['imagen_url']
        pais = paises_info[i]['pais']
        imagen_pais_url = paises_info[i]['imagen_url']

        document = {
            "año": año,
            "club": club,
            "imagen_club_url": imagen_club_url,
            "jugador": jugador,
            "imagen_jugador_url": imagen_jugador_url,
            "pais": pais,
            "imagen_pais_url": imagen_pais_url
        }

        if not collection.find_one({"año": año, "jugador": jugador}):
            collection.insert_one(document)
        else:
            print(f"El documento para el año {año} y jugador {jugador} ya existe.")

    print("Ganadores Balón de Oro subidos a MongoDB.")

cargarBalonesDeOro()
