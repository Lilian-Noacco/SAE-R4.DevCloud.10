from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import requests
from datetime import datetime
from babel.dates import format_datetime

app = Flask(__name__)
app.secret_key = 'votre-cle-secrete'

# Configuration de l'URL de base de l'API DRF
API_BASE_URL = "http://127.0.0.1:8000/api/"


def format_date(date_str):
    try:
        date_obj = datetime.fromisoformat(date_str)
        return format_datetime(date_obj, 'EEEE d MMMM yyyy \'à\' HH\'h\'mm', locale='fr_FR')
    except ValueError as e:
        # Gestion des erreurs de format de date
        print(f"Erreur de formatage de date: {e}")
        return date_str


@app.route('/')
def index():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}vols/", headers=headers)
    vols = response.json()
    # Formater les dates
    for vol in vols:
        vol['vol_date_depart'] = format_date(vol['vol_date_depart'])
        vol['vol_date_arrive'] = format_date(vol['vol_date_arrive'])
    return render_template('vols.html', vols=vols)

@app.route('/paiement/<reservation_id>', methods=['GET', 'POST'])
def paiement(reservation_id):

    headers = {'Authorization': f'Token {session.get("token")}'}
    if request.method == 'POST':
        data = {
            'achat_iban': request.form['achat_iban'],
            'achat_reservation': reservation_id,
        }

        headers = {'Authorization': f'Token {session.get("token")}'}
        response = requests.post(f"{API_BASE_URL}achat/", json=data, headers=headers)

        if response.status_code == 201:
            return redirect(url_for('get_achats'))
        else:
            return response.json(), response.status_code
    else:
        return render_template('achat.html')

@app.route('/achats')
def get_achats():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}achat/", headers=headers)
    achats = response.json()
    print(achats)
    for achat in achats:
        achat['achat_date_prelevement'] = format_date(achat['achat_date_prelevement'])

    print(achats)
    return render_template('achats.html', achats=achats)

@app.route('/checkout')
def make_achats():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}achat/", headers=headers)
    achats = response.json()
    for achat in achats:
        achat['achat_date_prelevement'] = format_date(achat['achat_date_prelevement'])

    print(achats)
    return render_template('achats.html', achats=achats)

@app.route('/reservations')
def get_reservations():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}reservation/", headers=headers)
    reservations = response.json()

    response = requests.get(f"{API_BASE_URL}vols/", headers=headers)
    vols = response.json()
    # Formater les dates
    for vol in vols:
        vol['vol_date_depart'] = format_date(vol['vol_date_depart'])
        vol['vol_date_arrive'] = format_date(vol['vol_date_arrive'])
    # for reservation in reservations:
    #     reservation['reservation_date_creation'] = format_date(reservation['reservation_date_creation'])
    #     reservation['vol_complet'] = vols[reservation['reservation_vol']]
    return render_template('reservations.html', reservations=reservations, vols=vols)


@app.route('/reservation/<vol_id>', methods=['GET', 'POST'])
def make_reservation(vol_id):
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}vol/{vol_id}/", headers=headers)
    vol = response.json()

    vol['vol_date_depart'] = format_date(vol['vol_date_depart'])
    vol['vol_date_arrive'] = format_date(vol['vol_date_arrive'])
    if request.method == 'POST':
        data = {
            'reservation_nombre_personne': request.form['reservation_nombre_personne'],
            'reservation_vol': vol_id
        }

        headers = {'Authorization': f'Token {session.get("token")}'}
        response = requests.post(f"{API_BASE_URL}reservation/", json=data, headers=headers)

        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            return response.json(), response.status_code
    else:
        return render_template('reserver.html', vol=vol)


@app.route('/login_register')
def login_register():
    return render_template('login_register.html')


@app.route('/login', methods=['POST'])
def login():
    data = {
        'username': request.form['username'],
        'password': request.form['password']
    }
    response = requests.post(f"{API_BASE_URL}login/", json=data)
    if response.status_code == 200:
        session['token'] = response.json().get('token')
        return redirect(url_for('index'))
    return response.json()


@app.route('/register', methods=['POST'])
def register():
    data = {
        'username': request.form['username'],
        'email': request.form['email'],
        'password': request.form['password'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    response = requests.post(f"{API_BASE_URL}register/", json=data)
    if response.status_code == 200:
        user_data = response.json()
        session['token'] = user_data.get('token')
        return redirect(url_for('index'))
    return response.json()


@app.route('/test')
def test_login():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}test_login/", headers=headers)
    achats = response.json()
    return jsonify(achats)


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))


@app.route('/paiement')
def get_paiement():
    headers = {'Authorization': f'Token {session.get("token")}'}
    response = requests.get(f"{API_BASE_URL}achat/", headers=headers)
    paiement = response.json()
    if request.method == 'POST':
        data = {
            'card-number': request.form['card-number'],
            'card-holder': request.form['card-holder'],
            'expiry-date': request.form['expiry-date'],
            'cvv': request.form['cvv'],

        }

        headers = {'Authorization': f'Token {session.get("token")}'}
        response = requests.post(f"{API_BASE_URL}paiement/", json=data, headers=headers)

    else:
        return render_template('paiement.html', paiement=paiement)




if __name__ == '__main__':
    app.run(debug=True)
