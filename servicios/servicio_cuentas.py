from flask import jsonify

from config.db import obtener_conexion
from servicios.servicio_auth import encripta_password, compara_password


def obtener_cuentas():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("Select * from cuentas")
    db = cursor.fetchall()
    cuentas = []
    for cuenta in db:
        cuenta_tojson = {
            'id': cuenta[0],
            'usuario': cuenta[1],
            "correo": cuenta[3],
            "roles": cuenta[4]
        }
        cuentas.append(cuenta_tojson)
    conn.commit()
    conn.close()
    return cuentas


def obtener_cuenta(_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario, correo, roles FROM cuentas WHERE id = %s", (_id,))
    db = cursor.fetchone()
    cursor.close()
    conn.close()
    if not db:
        return None

    return {
        "id": _id,
        "usuario": db[0],
        "correo": db[1],
        "roles": db[2]
    }


def verifica_usuario(usuario):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cuentas WHERE usuario = %s', (usuario,))
    cuenta = cursor.fetchone()
    if cuenta:
        return False
    else:
        return True


def crear_cuenta(cuenta):
    conn = obtener_conexion()
    password = cuenta.get('password')
    usuario = cuenta.get('usuario')
    if verifica_usuario(usuario):
        cursor = conn.cursor()
        hash_password = encripta_password(password)
        cursor.execute("INSERT INTO cuentas(id,usuario, password, correo, roles) VALUES (%s, %s, %s, %s, %s)",
                       (0, cuenta.get('usuario'), hash_password, cuenta.get('correo'), cuenta.get('roles')))
        filas_afectadas = cursor.rowcount
        id_cuenta = cursor.lastrowid
        cuenta['id'] = id_cuenta
        conn.commit()
        conn.close()
        if filas_afectadas == 0:
            return False
        return cuenta
    return False


def actualizar_cuenta(cuenta, _id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE cuentas SET usuario = %s, correo = %s WHERE id = %s",
                   (cuenta.get('usuario'), cuenta.get('correo'), _id))
    filas_afectadas = cursor.rowcount
    conn.commit()
    conn.close()
    if filas_afectadas == 0:
        return jsonify(error="No se ha actualizado ninguna cuenta"), 500
    return jsonify(cuenta), 200


def actualizar_password(_id, password, new_password):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM cuentas WHERE id = %s', (_id,))
    stored_hashed_password = cursor.fetchone()[0]
    if compara_password(password, stored_hashed_password):
        hash_password = encripta_password(new_password)
        cursor.execute('UPDATE cuentas SET password = %s WHERE id = %s', (hash_password, _id))
        filas_afectadas = cursor.rowcount
        conn.commit()
        cursor.close()
        if filas_afectadas == 0:
            return jsonify("no se a podido actualizar la contraseña"), 400
        else:
            return jsonify("contraseña actualizada con exito!"), 200
    return jsonify("la contraseña ingresada no es valida!"), 400


def eliminar_cuenta(_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cuentas WHERE id = %s', (_id,))
    filas_afectadas = cursor.rowcount
    conn.commit()
    cursor.close()
    if filas_afectadas == 0:
        return False
    else:
        return True
