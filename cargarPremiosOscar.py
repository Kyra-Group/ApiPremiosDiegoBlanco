import requests
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://apipremiosdiegoblanco.onrender.com/api/nominations"
response = requests.get(url)
data = response.json()['nominations']

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client['PremiosOscar']
collection = db['Ganadores']

for nomination in data:
    category = nomination['category']
    year = nomination['year']
    nominees = nomination['nominees']
    movies = nomination['movies']

    for movie in movies:
        title = movie['title']
        if title in nominees:
            nominees = [title]

    if len(nominees) == 1:
        nominees = nominees[0] 

    document = {
        "category": category,
        "year": year,
        "nominees": nominees
    }
    collection.insert_one(document)
