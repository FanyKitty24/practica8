from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
from mysql.connector import pooling
import datetime
import pytz
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db_config = {
    "host": "82.197.82.90",
    "user": "u861594054_fanysl06",
    "password": "f9GQT5Bq9M]",
    "database": "u861594054_prac4_awi"
}

# Creación de un pool de conexiones para mejorar el manejo de sesiones
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    **db_config
)

# Función para obtener una conexión del pool
def conectar_bd():
    return connection_pool.get_connection()

# Ruta para obtener las asistencias desde la vista `vistas`
@app.route('/asistencias', methods=['GET'])
@cross_origin()
def obtener_asistencias():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vistas")
        asistencias = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(asistencias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para registrar una nueva asistencia
@app.route('/asistencias', methods=['POST'])
@cross_origin()
def registrar_asistencia():
    try:
        data = request.get_json()
        idEmpleado = data.get("idEmpleado")
        idReporte = data.get("idReporte")
        estado = data.get("estado", "A")  # Estado por defecto 'A'
        if not idEmpleado or not idReporte:
            return jsonify({"error": "Faltan datos obligatorios"}), 400
        conn = conectar_bd()
        cursor = conn.cursor()
        query = "INSERT INTO asistencias (idEmpleado, idReporte, estado) VALUES (%s, %s, %s)"
        cursor.execute(query, (idEmpleado, idReporte, estado))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Asistencia registrada correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
