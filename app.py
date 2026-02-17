from flask import Flask, request, render_template, jsonify, session, redirect, url_for, flash, g
import sqlite3
from datetime import datetime
import json
from functools import wraps
import hashlib

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'Sistema-secret-key-2025'  # Necesario para sessions

#Conexion a la base de datos:
DATABASE = '/home/hernansote/dbs/sys-reportes/sys-reportes'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db 


#Rutas pricipales
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/registro")
def registro():
   # Ensure the user reached path via GET
   if request.method == "GET":
      return render_template("registro.html")


#sistema de login y registro

@app.route('/registrodata', methods = ['POST'])
def registrodata():
    content = request.get_json()
    name =  content.get("name")
    email = content.get("email")
    password = content.get("password")

    if not name or not email or not password:
        return jsonify ({"error": "se requiere llenar todos los espacios"}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:   
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password) )
        conn.commit()
        new_id = cursor.lastrowid
        new_registry = {
            "id": new_id,
            "name": name,
            "email": email,
        }
        return jsonify ({"message": "Usuario registrado", "usuario": new_registry}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error:" "El usuario ya existe"}), 409

@app.route("/logindata", methods=['POST'])
def logindata():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify ({"error": "Falta el usuario o contraseña"}), 409

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password)).fetchone()
    
    if user:
        return jsonify ({"message": f"bienvenido {email}"})
    else:
        return jsonify ({"error": "credenciales invalidas"}), 400

    

    

#Inicializacion
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3030)