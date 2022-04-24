# este es un comentario
# 1ero - importar código necesario
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
from flask_cors import CORS
import sqlalchemy
from sqlalchemy import *

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
