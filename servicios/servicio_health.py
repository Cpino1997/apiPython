from flask import jsonify

from config.db import obtener_conexion


def check_status():
    db_status = check_database()
    if db_status:
        return jsonify(mensaje="funcionando!"), 200
    return jsonify(error="no es posible establecer conexion "), 500


def check_database():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        conn.close()
        return True

    except Exception as e:
        print(e)
        return False


# HealthCheck
health_status = True


def toggle():
    global health_status
    health_status = not health_status
    return jsonify(health_value=health_status)


def health():
    if health_status:
        resp = jsonify(health="vivo")
        resp.status_code = 200
    else:
        resp = jsonify(health="muerto")
        resp.status_code = 500
    return resp
