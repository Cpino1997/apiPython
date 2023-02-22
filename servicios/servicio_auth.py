import bcrypt
from flask import jsonify
from flask_jwt_extended import create_access_token

from config.db import obtener_conexion


def login(usuario, password):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM cuentas WHERE usuario = %s', (usuario,))
    stored_hashed_password = cursor.fetchone()[0]
    cursor.close()
    if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s', (usuario,))
        db = cursor.fetchone()
        cursor.close()
        if db:
            access_token = create_access_token(identity=usuario)
            return jsonify(access_token=access_token), 200
        error_resp = jsonify(success=False, mensaje='Usuario o contraseña incorrecta')
        error_resp.status_code = 400
        return error_resp
    return jsonify(error="la contraseña ingresada no es valida!"), 400


def encripta_password(password):
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_password


def compara_password(password, store_password):
    if bcrypt.checkpw(password.encode(), store_password.encode()):
        return True
    else:
        return False


def get_rol(usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT roles FROM cuentas WHERE usuario = %s', (usuario,))
    roles = cursor.fetchone()
    cursor.close()
    return roles[0]


