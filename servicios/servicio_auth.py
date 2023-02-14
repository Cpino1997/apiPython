import time

import bcrypt
from flask import session, jsonify

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
        cuenta = cursor.fetchone()
        cursor.close()
        if cuenta:
            columns = [col[0] for col in cursor.description]
            cuenta = dict(zip(columns, cuenta))
            session['loggedin'] = True
            session['id'] = cuenta['id']
            session['usuario'] = cuenta['usuario']
            session['roles'] = cuenta['roles']
            session['tiempo_sesion'] = time.time()
            return jsonify(mensaje='Inicio de sesión exitoso', session=session, cuenta=cuenta), 200
    else:
        return jsonify(success=False, mensaje='Usuario o contraseña incorrecta'), 400


def encripta_password(password):
    hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash_password


def compara_password(password, store_password):
    if bcrypt.checkpw(password.encode(), store_password.encode()):
        return True
    else:
        return False


def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('usuario', None)
    session.clear()
    return jsonify({"mensaje": "Session eliminada con exito!"}), 200


def get_session():
    session_dto = {'usuario': session['usuario'], 'loggedin': session['loggedin'],
                   'tiempo_sesion': session['tiempo_sesion']}
    return jsonify(session_dto)


def get_rol(usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT roles FROM cuentas WHERE usuario = %s', (usuario,))
    roles = cursor.fetchone()
    cursor.close()
    return roles
