from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Función para conectar a MySQL
def conectar():
    return mysql.connector.connect(
        host="82.197.82.90",
        database="u861594054_app9",
        user="u861594054_Misael2009",
        password="NZqhQyiNZ3Tg8JJ"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app")
def app2():
    return "<h5>Hola, soy la view app</h5>"

@app.route("/asistencias")
def asistencias():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT `idAsistencia`, `empleado`, `reporte` FROM `vistatotal` LIMIT 10 OFFSET 0"  # Arreglado el doble `reporte`
    cursor.execute(sql)
    registros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("asistencias.html", asistencias=registros)

@app.route("/empleados")
def empleados():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT `idEmpleado`, `nombreEmpleado`, `numero`, `fechaIngreso` FROM empleados LIMIT 10 OFFSET 0"
    cursor.execute(sql)
    registros = cursor.fetchall()

    # Si manejas fechas y horas
    for registro in registros:
        fecha_hora = registro["fechaIngreso"]
        if fecha_hora:  # Verifica si no es None
            registro["Fecha_Hora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")

    cursor.close()
    conn.close()
    return render_template("empleados.html", empleados=registros)

@app.route("/reportes")
def reportes():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT `idReporte`, `fecha`, `comentarios` FROM `reportes` LIMIT 10 OFFSET 0"
    cursor.execute(sql)
    registros = cursor.fetchall()

    # Si manejas fechas y horas
    for registro in registros:
        fecha_hora = registro["fecha"]
        if fecha_hora:  # Verifica si no es None
            registro["Fecha"] = fecha_hora.strftime("%d/%m/%Y")

    cursor.close()
    conn.close()
    return render_template("reportes.html", reportes=registros)
