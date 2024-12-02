from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/oscar-nominations', methods=['GET'])
def get_oscar_nominations():
    # URL del archivo JSON
    url = 'https://raw.githubusercontent.com/delventhalz/json-nominations/main/oscar-nominations.json'
    
    # Obtener los datos del JSON
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa (200 OK)
        return jsonify(response.json())  # Retorna los datos JSON como respuesta
    except requests.exceptions.RequestException as e:
        # En caso de error, retorna un mensaje de error
        return jsonify({'error': 'No se pudo obtener los datos', 'details': str(e)}), 500

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
