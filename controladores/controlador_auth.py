from flask import request, Blueprint, jsonify

from controladores.validadores import login_required, rol_required
from servicios import servicio_auth

bp_auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp_auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        usuario = data.get('usuario')
        password = data.get('password')
        if not usuario:
            return jsonify(error="debe ingresar un usuario"), 500
        if not password:
            return jsonify(error="debe ingresar una contraseña"), 500
        cuenta = servicio_auth.login(usuario, password)
        return cuenta


@bp_auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    mensaje = servicio_auth.logout()
    return mensaje


@bp_auth.route("/session", methods=["POST", "GET"])
@login_required
def get_session():
    mensaje = servicio_auth.get_session()
    return mensaje


@bp_auth.route("/testuser", methods=["GET"])
@login_required
@rol_required("user")
def testUser():
    return jsonify("funcionando")
