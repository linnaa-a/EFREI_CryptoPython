from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, current_app
from flask import render_template_string, jsonify
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(name)

@app.route('/')
def hello_world():
    return render_template('hello.html')

--- Clé persistante pour que les tokens restent valides ---
KEY_FILE = "secret.key"
try:
    with open(KEY_FILE, "rb") as fkey:
        key = fkey.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as fkey:
        fkey.write(key)

f = Fernet(key)

--- Route d'encryptage existante ---
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

--- NOUVELLE ROUTE : /decrypt/ ---
@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())  # Déchiffre le token
        valeur = valeur_bytes.decode()
        return f"Valeur déchiffrée : {valeur}"
    except InvalidToken:
        return "Erreur : le token fourni est invalide ou la clé ne correspond pas.", 400
    except Exception as e:
        current_app.logger.exception("Erreur de décryptage")
        return f"Erreur interne : {str(e)}", 500

if name == "main":
    app.run(debug=True)
