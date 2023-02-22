from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies, current_user, get_jwt_identity, create_access_token
from servicios import servicio_auth

from utils.validadores import validate_input, rol_required

bp_auth = Blueprint('auth', __name__, url_prefix='/api/auth')

blacklist = set()


@bp_auth.route("/login", methods=['GET', 'POST'])
@validate_input
def login():
    usuario = request.json.get('usuario', None)
    password = request.json.get('password', None)
    response = servicio_auth.login(usuario, password)
    return response


@bp_auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@bp_auth.route("/user", methods=["GET"])
@jwt_required()
@rol_required("user")
def test_user():
    return jsonify("funcionando"), 200


@bp_auth.route("/admin", methods=["GET"])
@jwt_required()
@rol_required("admin")
def test_admin():
    return jsonify("funcionando"), 200


@bp_auth.route('/verify')
@jwt_required()
def verify():
    return jsonify({'mensaje': 'Ruta protegida'})


@bp_auth.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token})
