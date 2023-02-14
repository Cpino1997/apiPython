import time
from functools import wraps

from flask import jsonify, session, Blueprint
import re

validadores = Blueprint('validadores', __name__)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            tiempo_actual = time.time()
            tiempo_sesion = session.get('tiempo_sesion', tiempo_actual)
            tiempo_transcurrido = tiempo_actual - tiempo_sesion
            if tiempo_transcurrido > 1800:  # 30 minutos
                session.clear()
                return jsonify(message='Su sesión ha expirado, por favor inicie sesión nuevamente para continuar'), 401
            else:
                session['tiempo_sesion'] = tiempo_actual
                return f(*args, **kwargs)
        else:
            return jsonify(message='No estas autorizado para acceder a este recurso'), 401

    return wrap


def rol_required(rol):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'loggedin' in session:
                role = session['roles']
                if rol == role:
                    return func(*args, **kwargs)
                else:
                    return jsonify(error="no estas autorizado para acceder a este recurso!"), 401

        return wrapper

    return decorator


def valida_correo(correo):
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    match = pattern.match(correo)
    return match


def validaPassword(password):
    if password == '':
        return jsonify(error="Debe ingresar una Contraseña!"), 400
    if len(password) < 4:
        return jsonify(error="la contraseña debe tener al menos 4 caracteres!"), 400
    mayusculas = 0
    numeros = 0
    for char in password:
        if char.isupper():
            mayusculas += 1
        elif char.isdigit():
            numeros += 1
    if mayusculas < 1:
        return jsonify(error="la contraseña debe tener 1 letra mayúscula!"), 400
    if numeros < 2:
        return jsonify(error="la contraseña debe tener 2 números!"), 400


def validaData(user):
    usuario = user.get('usuario')
    correo = user.get('correo')
    password = user.get('password')
    roles = user.get('roles')
    if not roles:
        user['roles'] = "user"
    if not usuario:
        return jsonify(error="el usuario no puede estar vacio!"), 400
    if len(usuario) <= 6:
        return jsonify(error="el usuario debe tener mas de 6 caracteres!"), 400
    if len(usuario) >= 20:
        return jsonify(error="el usuario no debe tener mas de 20 caracteres!"), 400
    if correo == '':
        return jsonify(mensaje="el correo no puede estar vacio!"), 400
    if len(correo) <= 10:
        return jsonify(error="el correo debe tener mas de 10 caracteres!"), 400
    if len(correo) >= 50:
        return jsonify(error="el correo debe tener como maximo 50 caracteres !"), 400
    if not valida_correo(correo):
        return jsonify(error="ingrese un correo no válido"), 400
    validaPassword(password)
    return user
