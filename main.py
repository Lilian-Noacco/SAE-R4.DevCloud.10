from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime
from babel.dates import format_datetime

app = Flask(__name__)

# Configuration de l'URL de base de l'API DRF
API_BASE_URL = "http://127.0.0.1:8000/"

@app.route('/')
def index():
    return "Bienvenue à l'application Flask client pour l'API DRF"

def format_date(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str)
        return format_datetime(date_obj, 'EEEE d MMMM yyyy \'à\' HH\'h\'mm', locale='fr_FR')
    except ValueError as e:
        # Gestion des erreurs de format de date
        print(f"Erreur de formatage de date: {e}")
        return date_str

@app.route('/vols')
def get_vols():
    response = requests.get(f"{API_BASE_URL}api/")
    print(response)
    vols = response.json()

    # Formater les dates
    for vol in vols:
        vol['vol_date_depart'] = format_date(vol['vol_date_depart'])
        vol['vol_date_arrive'] = format_date(vol['vol_date_arrive'])

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