import requests

def cargarPremiosOscar():
    # Cambia esta URL después de desplegar la API en Render
    api_url = "https://tu-api-en-render.com/winners"  

    url = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for item in data:
            if item.get('won') and item.get('movies'):
                year = item.get('year', '')
                category = item.get('category', '')
                nominees = item.get('nominees', [None])
                movie = item['movies'][0]
                movie_title = movie.get('title', '')

                nominee_to_store = nominees[0] if nominees[0] != movie_title else None

                document = {
                    "year": year,
                    "category": category,
                    "movie_title": movie_title,
                }

                if nominee_to_store:
                    document["nominee"] = nominee_to_store

                # Enviar el documento a la API FastAPI
                api_response = requests.post(api_url, json=document)

                if api_response.status_code == 201:
                    print(f"Ganador añadido correctamente: {document}")
                else:
                    print(f"Error al añadir ganador: {document} - {api_response.status_code}")
    else:
        print(f"Error al obtener los datos de la API original: {response.status_code}")

cargarPremiosOscar()
