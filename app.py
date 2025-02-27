from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime
import pytz
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
db_config = {
    "host": "127.0.0.1",
    "user": "tu_usuario",
    "password": "tu_contraseña",
    "database": "u861594054_prac4_awi"
}

# Función para conectar a la base de datos
def conectar_bd():
    return mysql.connector.connect(**db_config)

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
        id_empleado = data.get("idEmpleado")
        id_reporte = data.get("idReporte")
        estado = data.get("estado", "A")  # Estado por defecto 'A'

        if not id_empleado or not id_reporte:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        conn = conectar_bd()
        cursor = conn.cursor()

        query = "INSERT INTO asistencias (idEmpleado, idReporte, estado) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_empleado, id_reporte, estado))
        conn.commit()
        
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Asistencia registrada correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
