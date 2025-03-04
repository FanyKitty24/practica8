from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
from mysql.connector import pooling
import datetime
import pytz
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos utilizando variables de entorno 
# (Render permite definirlas en el panel de configuración)
db_config = {
    "host": os.environ.get("DB_HOST", "82.197.82.90"),
    "user": os.environ.get("DB_USER", "u861594054_fanysl06"),
    "password": os.environ.get("DB_PASSWORD", "f9GQT5Bq9M]"),
    "database": os.environ.get("DB_DATABASE", "u861594054_prac4_awi"),
    # Si tu servidor MySQL no requiere SSL, esta opción puede ayudar:
    "ssl_disabled": True
}

# Creación del pool de conexiones
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    **db_config
)

# Función para obtener una conexión del pool
def conectar_bd():
    return connection_pool.get_connection()

# Endpoint para obtener las asistencias desde la vista 'vistas'
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

# Endpoint para registrar una nueva asistencia
@app.route('/asistencias', methods=['POST'])
@cross_origin()
def registrar_asistencia():
    try:
        data = request.get_json()
        idEmpleado = data.get("idEmpleado")
        idReporte = data.get("idReporte")
        estado = data.get("estado", "A")  # Valor por defecto 'A'
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
