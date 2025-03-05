# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import pytz

from flask_cors import CORS, cross_origin

con = mysql.connector.connect(
    host="82.197.82.90",
    database="u861594054_prac4_awi",
    user="u861594054_fanysl06",
    password="R&6412^1a7"
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("index.html")

@app.route("/app")
def app2():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return "<h5>Hola, soy Fany ;)</h5>"

@app.route("/asistencias")
def asistencias():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idAsistencia,
           idEmpleado,
           idReporte,
           estado

    FROM asistencias

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()


    return render_template("asistencias.html", asistencias=asistencias)

@app.route("/asistencias/buscar", methods=["GET"])
def buscarProductos():
    if not con.is_connected():
        con.reconnect()

    args     = request.args
    busqueda = args["busqueda"]
    busqueda = f"%{busqueda}%"
    
    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idAsistencia,
           idEmpleado,
           idReporte,
           estado

    FROM asistencias

    WHERE idEmpleado LIKE %s
    OR    idReporte          LIKE %s
    OR    estado     LIKE %s

    ORDER BY idAsistencia DESC

    LIMIT 10 OFFSET 0
    """
    val    = (busqueda, busqueda, busqueda)

    try:
        cursor.execute(sql, val)
        registros = cursor.fetchall()


    except mysql.connector.errors.ProgrammingError as error:
        print(f"Ocurrió un error de programación en MySQL: {error}")
        registros = []

    finally:
        con.close()

    return make_response(jsonify(registros))

@app.route("/asistencia", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def guardarAsistencia():
    if not con.is_connected():
        con.reconnect()

    id          = request.form["id"]
    empleado      = request.form["empleado"]
    reporte      = request.form["reporte"]
    estado = request.form["estado"]
    # fechahora   = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE asistencias

        SET idEmpleado = %s,
            idReporte          = %s,
            estado     = %s

        WHERE idAsistencia = %s
        """
        val = (empleado, reporte, estado, id)
    else:
        sql = """
        INSERT INTO asistencias (idEmpleado, idReporte, estado)
                    VALUES    (%s,          %s,      %s)
        """
        val =                 (empleado, reporte, estado)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

@app.route("/asistencia/<int:id>")
def editarAsistencia(id):
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT idAsistencia, idEmpleado, idReporte, estado

    FROM asistencias

    WHERE idAsistencia = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/asistencia/eliminar", methods=["POST"])
def eliminarAsistencia():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    DELETE FROM asistencia
    WHERE idAsistencia = %s
    """
    val    = (id,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))
