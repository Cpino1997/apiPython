from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from servicios import servicio_cuentas
from utils.validadores import valida_cuenta

bp_cuentas = Blueprint('cuentas', __name__, url_prefix='/api')


@bp_cuentas.route("/cuentas", methods=['GET'])
@jwt_required()
def get_cuentas():
    cuentas = servicio_cuentas.get_cuentas()
    if cuentas is None:
        return jsonify(sucess="false", error="No se encontraron cuentas"), 404
    return cuentas


@bp_cuentas.route("/cuentas/<_id>", methods=['GET'])
@jwt_required()
def get_cuenta(_id):
    cuenta = servicio_cuentas.get_cuenta_id(_id)
    if cuenta is None:
        return jsonify(error="No se a encontrado ninguna cuenta!"), 404
    return jsonify(cuenta), 200


@bp_cuentas.route("/cuentas", methods=['POST'])
@jwt_required()
def post_cuenta():
    data = request.get_json()
    cuenta = valida_cuenta(data)
    response = servicio_cuentas.post_cuenta(cuenta)
    return response


@bp_cuentas.route("/cuentas/<_id>", methods=['PUT'])
@jwt_required()
def put_cuenta(_id):
    data = request.get_json()
    data['password'] = 123
    cuenta = valida_cuenta(data)
    response = servicio_cuentas.put_cuenta(_id, cuenta)
    return response


@bp_cuentas.route("/auth/password/<_id>", methods=['PUT'])
@jwt_required()
def put_password(_id):
    data = request.get_json()
    response = servicio_cuentas.put_password(data, _id)
    return response


@bp_cuentas.route("/cuentas/<_id>", methods=['DELETE'])
@jwt_required()
def delete_cuenta(_id):
    cuenta = servicio_cuentas.eliminar_cuenta(_id)
    if cuenta:
        return jsonify("se a eliminado con exito la cuenta!"), 200
    else:
        return jsonify("no se a podido eliminar la cuenta con exito :C"), 400


@bp_cuentas.route("/cuentas/get", methods=['GET'])
@jwt_required()
def get_cuenta_identity():
    identity = get_jwt_identity()
    cuenta = servicio_cuentas.get_cuenta_identity(identity)
    return cuenta
