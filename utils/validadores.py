from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from servicios.servicio_auth import get_rol


def validate_input(func):
    def wrapper(*args, **kwargs):
        usuario = request.json.get('usuario')
        password = request.json.get('password')
        if not usuario:
            return jsonify(error="Debe ingresar un usuario"), 400
        if not password:
            return jsonify(error="Ingrese una contraseña"), 400
        return func(*args, **kwargs)

    return wrapper


def rol_required(rol):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = get_jwt_identity()
            role = get_rol(usuario)
            if role == rol:
                return func(*args, **kwargs)
            else:
                return jsonify(error="No estás autorizado para acceder a este recurso"), 401

        return wrapper

    return decorator


def valida_cuenta(cuenta):
    if cuenta.get('usuario') is None:
        return jsonify(error="ingrese un usuario"), 400
    if cuenta.get('password') is None:
        return jsonify(error="ingrese una contraseña"), 400
    if cuenta.get('correo') is None:
        return jsonify(error="ingrese un correo"), 400
    if cuenta.get('roles') is None:
        cuenta['roles'] = "user"
        return cuenta


def valida_password(datos):
    password = datos.get('password')
    new_password = datos.get('new_password')
    if password is None:
        return False
    if new_password is None:
        return False
    return True
