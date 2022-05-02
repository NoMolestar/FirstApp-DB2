import re
from sqlite3 import connect
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
from flask_cors import CORS, cross_origin
from sqlalchemy import *
import sqlalchemy
import sys
import ibm_db_sa
import flask_login
import secrets
import flask

app = Flask(__name__)

app.config['DB2_DATABASE'] = 'testdb'
app.config['DB2_HOSTNAME'] = 'localhost'
app.config['DB2_PORT'] = 50000
app.config['DB2_PROTOCOL'] = 'TCPIP'
app.config['DB2_USER'] = 'db2inst1'
app.config['DB2_PASSWORD'] = 'hola'

db = DB2(app)

CORS(app)

# CÓDIGO PARA LOGIN
app.secret_key = secrets.token_urlsafe(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def get_db():
    engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
    return engine.connect()



class Usuario(flask_login.UserMixin):
    role = 0
    pass


@login_manager.user_loader
def user_loader(email):
    print("user_loader")
    conn = get_db()

    emailExists = conn.execute("SELECT email FROM users WHERE email = ?", (email,)).fetchone()

    role = conn.execute("SELECT role FROM users WHERE email = ?", (email,)).fetchone()[0]
    print("LOADER: role", role)
    
    if emailExists:
        return
    usuario = Usuario()
    usuario.id = email
    usuario.role = role
    return usuario

# método que se invoca para obtención de usuarios cuando se hace request


@login_manager.request_loader
def request_loader(request):
    print("request_loader")
    key = request.headers.get('Authorization')
    print(key, file=sys.stdout)

    if key == ":" or key is None:
        return None

    processed = key.split(":")

    conn = get_db()
    result = conn.execute("SELECT * FROM users WHERE email = ?", (processed[0],))
    userDB = result.fetchone()

    if userDB is not None and processed[1] == userDB[1]:
        user = Usuario()
        user.id = processed[0]
        user.role = userDB[2]
        return user

    return None


@app.route('/login', methods=['POST'])
def login():
    email = flask.request.form['email']
    password = flask.request.form['pass']

    try:
        connection = get_db()
        result = connection.execute("SELECT * FROM users WHERE email = '{}'".format(email))

        user = result.first()

        if user is not None and password == user[1]:
            usuario = Usuario()
            usuario.id = email
            usuario.role = user[2]
            flask_login.login_user(usuario)
            return jsonify({"success": "Login exitoso", "role": user[2]})
        return "CREDENCIALES INVÁLIDAS", 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error al conectar con la base de datos"}), 500

@app.route('/register', methods=['POST'])
def register():
    email = flask.request.form['email']
    password = flask.request.form['password']
    try:
        connection = get_db()
        emailExists = connection.execute("SELECT * FROM USERS WHERE email = '" + email + "'")


        if emailExists.first() is not None:
            return "EMAIL YA EXISTE", 401

        connection.execute("INSERT INTO USERS (email, password, role) VALUES ('" + email + "', '" + password + "', 0)")
        
        return "USUARIO REGISTRADO", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/protegido')
@cross_origin()
def protegido():
    return jsonify(protegido=flask_login.current_user.is_authenticated)


@login_manager.unauthorized_handler
def handler():
    return 'No autorizado', 401


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'saliste'


@app.route("/")
def index():
    return "Hola mundo", 200


@app.route("/select")
@cross_origin()
@flask_login.login_required
def select():
    try:
        engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
        conn = engine.connect()
        result = conn.execute("SELECT id, name FROM products")
        response = []
        for current in result:
            actual = {
                "id": current[0],
                "name": current[1],
            }
            response.append(actual)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/select/<int:valor>", methods=["GET"])
@cross_origin()
@flask_login.login_required
def selectID(valor):
    print("User role: " + str(flask_login.current_user.role))
    try:
        engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
        conn = engine.connect()
        result = conn.execute(
            "SELECT * FROM products WHERE id = " + str(escape(valor)))
        response = None
        for current in result:
            actual = {
                "id": current[0],
                "name": current[1],
                "price": current[2],
            }
            response = actual
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# podemos tener todas las rutas


@app.route("/createTable")
def createTable():
    try:
        engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
        engine.execute("DROP TABLE products IF EXISTS")
        engine.execute("DROP TABLE users IF EXISTS")
        engine.execute(
            "CREATE TABLE products (id INTEGER, name VARCHAR(20), price DOUBLE)")
        engine.execute(
            "CREATE TABLE IF NOT EXISTS users (email VARCHAR(64) NOT NULL PRIMARY KEY, password VARCHAR(32), role INTEGER)")
        return "Tabla creada", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/insertValues")
def insertValues():
    # Insert five products into the table
    try:
        engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
        engine.execute("DELETE FROM products")
        engine.execute("INSERT INTO products VALUES (1, 'Laptop', 1000)")
        engine.execute("INSERT INTO products VALUES (2, 'Mouse', 10)")
        engine.execute("INSERT INTO products VALUES (3, 'Keyboard', 20)")
        engine.execute("INSERT INTO products VALUES (4, 'Monitor', 200)")
        engine.execute("INSERT INTO products VALUES (5, 'Printer', 50)")
        engine.execute("INSERT INTO users VALUES ('admin@example.com', '123tamarindo', 1)")
        return "Valores insertados", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
