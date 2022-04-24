# este es un comentario
# 1ero - importar código necesario
from tokenize import Double
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
import sys
from flask_cors import CORS
import sqlalchemy
from sqlalchemy import *
import ibm_db_sa

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

# 3ero - al objeto de tipo flask le agregamos rutas
# @ en python significa que vamos a usar un decorator
# https://en.wikipedia.org/wiki/Decorator_pattern


@app.route("/")
def index():
    return "Hola mundo", 200


@app.route("/selectAll")
def selectAll():
    try:
        # lo primero es obtener cursor
        cur = db.connection.cursor()

        # con cursor hecho podemos ejecutar queries
        cur.execute("SELECT * FROM productos")

        # obtenemos datos
        data = cur.fetchall()

        # acuerdate de cerrar el cursor
        cur.close()

        print(data, file=sys.stdout)

        # puedes checar alternativas para mapeo de datos
        # por hoy vamos a armar un objeto jsoneable para regresar
        resultado = []
        for current in data:
            actual = {
                "id": current[0],
                "nombre": current[1],
                "precio": current[2]
            }
            resultado.append(actual)

        return jsonify(resultado)
    except:
        return "<h1>Ocurrió un error al mostrar la tabla.</h1>"


@app.route("/selectByID/<int:valor>", methods=["GET"])
def selectByID(valor):
    try:
        # lo primero es obtener cursor
        cur = db.connection.cursor()

        # con cursor hecho podemos ejecutar queries
        cur.execute("SELECT * FROM productos where id = ?", (escape(valor)))

        # obtenemos datos
        data = cur.fetchall()

        # acuerdate de cerrar el cursor
        cur.close()

        print(data, file=sys.stdout)

        # puedes checar alternativas para mapeo de datos
        # por hoy vamos a armar un objeto jsoneable para regresar
        resultado = []
        for current in data:
            actual = {
                "id": current[0],
                "nombre": current[1],
                "precio": current[2]
            }
            resultado.append(actual)

        return jsonify(resultado)
    except:
        return "<h1>Ocurrió un error al mostrar la tabla.</h1>"

# podemos tener todas las rutas


@app.route("/createTable")
def createTable():
    # Create table products with id, name and price
    cur = db.connection.cursor()
    cur.execute("DROP TABLE IF EXISTS productos")
    cur.execute(
        "CREATE TABLE productos (id INTEGER NOT NULL, nombre VARCHAR(20), precio INTEGER)")
    cur.close()
    return "<h1>Tabla creada</h1>"


@app.route("/insertValues")
def insertValues():
    # Insert five products into the table
    try:
        engine = sqlalchemy.create_engine(
            "ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
        connection = engine.connect()
        metadata = sqlalchemy.MetaData()
        productos = Table('productos', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('nombre', String(150), nullable=False),
                          Column('precio', Double, nullable=False)
                          )
        query = productos.insert().values(
            id=1, nombre='Leche', precio=10.0)
        connection.execute(query)
        query = productos.insert().values(
            id=2, nombre='Cereal', precio=20.0)
        connection.execute(query)
        query = productos.insert().values(
            id=3, nombre='Huevos', precio=30.0)
        connection.execute(query)
        query = productos.insert().values(
            id=4, nombre='Tortillas', precio=22.0)
        connection.execute(query)
        query = productos.insert().values(
            id=5, nombre='Frijoles', precio=350.0)
        connection.execute(query)
        return "<h1>Valores insertados con exito.</h1>"
    except:
        return "<h1>Ocurrió un error al insertar la tabla.</h1>"

# podemos recibir variables a través de URL
# f-string formatting
# &eacute; & e acute; - e con acento agudo
# ataque por inyección de código

# @app.route("/nombre/<el_nombre>/<el_apellido>")
# def nombre(el_nombre, el_apellido):
#     return f"Hola {escape(el_nombre)} {escape(el_apellido)}, espero que est&eacute;s bien."

# converters

# @app.route("/entero/<int:valor>")
# def entero(valor):
#     return f"el valor que mandaste fue: {escape(valor)}"

# @app.route("/ruta/<path:valor>")
# def ruta(valor):
#     return f"la ruta que mandaste fue: {escape(valor)}"

# LO QUE VAMOS A REGRESAR GENERALMENTE VA A SER JSON
# ventaja de flask - regresar un diccionario de python se jsonifica

# diccionario = {
#     "nombre": "Garfiol",
#     "edad": 30,
#     "peso": 64
# }

# @app.route("/json")
# def json():
#     return diccionario

# se puede discriminar por medio de método de request de HTTP
# (GET, POST, PUT, DELETE)

# @app.route("/metodo", methods=["GET", "POST"])
# def metodo_get_post():
#     return "REQUEST HECHA POR GET O POST"

# @app.route("/metodo", methods=["PUT", "DELETE"])
# def metodo_put_delete():
#     return "REQUEST HECHA POR PUT O DELETE"

# EXTENSION DE VS CODE - THUNDERCLIENT
