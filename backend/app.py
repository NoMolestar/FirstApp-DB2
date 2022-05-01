# este es un comentario
# 1ero - importar código necesario
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

# 2do - creamos un objeto de tipo flask
app = Flask(__name__)

# APLICAR CONFIG DE DB2
app.config['DB2_DATABASE'] = 'testdb'
app.config['DB2_HOSTNAME'] = 'localhost'
app.config['DB2_PORT'] = 50000
app.config['DB2_PROTOCOL'] = 'TCPIP'
app.config['DB2_USER'] = 'db2inst1'
app.config['DB2_PASSWORD'] = 'hola'

db = DB2(app)

CORS(app)

# CÓDIGO PARA LOGIN
# necesitamos una llave secreta
app.secret_key = secrets.token_urlsafe(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# PSEUDO BASE DE DATOS DE USUARIOS
usuarios = {"a@a.com": {"pass": "hola"}}

# definir una clase para contener la descripción de nuestros usuarios


class Usuario(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    # verificar vs fuente de datos
    if email not in usuarios:
        return

    usuario = Usuario()
    usuario.id = email
    return usuario

# método que se invoca para obtención de usuarios cuando se hace request


@login_manager.request_loader
def request_loader(request):

    # obtener información que nos mandan en encabezado
    key = request.headers.get('Authorization')
    print(key, file=sys.stdout)

    if key == ":":
        return None

    processed = key.split(":")

    if processed[0] in usuarios and processed[1] == usuarios[processed[0]]['pass']:
        user = Usuario()
        user.id = processed[0]
        return user

    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    # podemos verificar con qué método se accedió
    if flask.request.method == 'GET':
        return '''
                <form action='login' method='POST'>
                    <input type='text' name='email' /><br />
                    <input type='password' name='password' /><br />
                    <input type='submit' name='HACER LOGIN' />
                </form>
        
        '''

    # de otra manera tuvo que ser POST
    # obtener datos
    email = flask.request.form['email']

    # verificar validez de usuario vs fuente de datos
    if email in usuarios and flask.request.form['pass'] == usuarios[email]['pass']:
        user = Usuario()
        user.id = email
        flask_login.login_user(user)
        # OJO AQUI
        # esta es la parte en donde pueden generar un token
        # return flask.redirect(flask.url_for('protegido'))
        return "USUARIO VALIDO", 200

    # si no jaló mostrar error
    return "CREDENCIALES INVÁLIDAS", 401


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
def selectID(valor):
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
        engine.execute(
            "CREATE TABLE products (id INTEGER, name VARCHAR(20), price DOUBLE)")
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
        return "Valores insertados", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
