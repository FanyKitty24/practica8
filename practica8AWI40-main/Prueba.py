import mysql.connector

# Configuración de conexión
config = {
    "host": "82.197.82.90",
    "database": "u861594054_prac8_awi",
    "user": "u861594054_fany_sl06",
    "password": "g^2QY#GP@R"
}

try:
    # Intentar la conexión
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    # Ejecutar una consulta de prueba
    cursor.execute("SELECT NOW() AS fecha_hora;")  # Obtiene la fecha y hora del servidor MySQL
    resultado = cursor.fetchone()

    # Mostrar resultado
    print("Conexión exitosa. La fecha y hora en el servidor MySQL es:", resultado["fecha_hora"])

    # Cerrar conexión
    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print("Error al conectar a MySQL:", err)
