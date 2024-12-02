from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import requests

app = FastAPI()

URL = "https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json"

def fetch_data():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Error al obtener los datos de la API original")

@app.get("/")
def redirect_to_winners():
    return RedirectResponse(url="/winners/")

@app.get("/winners/")
def get_all_winners(limit: int = None):
    data = fetch_data()
    winners = [item for item in data if item.get("won")]
    if not winners:
        raise HTTPException(status_code=404, detail="No se encontraron ganadores")
    if limit:
        winners = winners[:limit]
    return {"count": len(winners), "winners": winners}

@app.get("/winners/{year}")
def get_winners_by_year(year: str):
    data = fetch_data()
    winners = [item for item in data if item.get("won") and item.get("year") == year]
    if not winners:
        raise HTTPException(status_code=404, detail=f"No se encontraron ganadores para el año {year}")
    return {"year": year, "count": len(winners), "winners": winners}

@app.get("/categories/{category}")
def get_winners_by_category(category: str):
    data = fetch_data()
    winners = [item for item in data if item.get("won") and item.get("category").lower() == category.lower()]
    if not winners:
        raise HTTPException(status_code=404, detail=f"No se encontraron ganadores en la categoría '{category}'")
    return {"category": category, "count": len(winners), "winners": winners}

@app.get("/movie/{title}")
def get_winner_by_movie(title: str):
    data = fetch_data()
    for item in data:
        if item.get("won"):
            movies = item.get("movies", [])
            for movie in movies:
                if movie.get("title").lower() == title.lower():
                    return {"category": item["category"], "year": item["year"], "movie": movie, "won": item["won"]}
    raise HTTPException(status_code=404, detail=f"No se encontró información para la película '{title}'")

