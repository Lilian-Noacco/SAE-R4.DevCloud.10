# app.py
from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# Configuration de l'URL de base de l'API DRF
API_BASE_URL = "http://127.0.0.1:8000/"  # Changez cela en fonction de l'URL de votre API DRF

@app.route('/')
def index():
    return "Bienvenue à l'application Flask client pour l'API DRF"

@app.route('/vols')
def get_vols():
    response = requests.get(f"{API_BASE_URL}api/")
    print(response)
    vols = response.json()
    return render_template('vols.html', vols=vols)


@app.route('/achats')
def get_achats():
    response = requests.get(f"{API_BASE_URL}achats/")
    achats = response.json()
    return jsonify(achats)

@app.route('/reservations')
def get_reservations():
    response = requests.get(f"{API_BASE_URL}reservations/")
    reservations = response.json()
    return jsonify(reservations)

if __name__ == '__main__':
    app.run(debug=True)
