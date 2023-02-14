from flask import jsonify, Blueprint, request

from controladores.validadores import validaData, login_required
from servicios import servicio_cuentas

bp_cuentas = Blueprint('cuentas', __name__, url_prefix='/api')


@bp_cuentas.route("/cuentas", methods=['GET', 'POST'])
@login_required
def obtener_crear_cuentas():
    if request.method == 'GET':
        cuentas = servicio_cuentas.obtener_cuentas()
        if not cuentas:
            return jsonify(error="No se encontraron cuentas"), 404
        return jsonify(cuentas), 200
    elif request.method == 'POST' and request.is_json:
        data = request.get_json()
        cuenta = validaData(data)
        cuenta = servicio_cuentas.crear_cuenta(cuenta)
        if cuenta:
            return cuenta
        else:
            return jsonify("el usuario ya se encuentra registrado!"), 400


@bp_cuentas.route("/cuentas/<_id>", methods=['GET', 'PUT', 'DELETE'])
@login_required
def obtener_cuenta(_id):
    if request.method == 'GET':
        cuenta = servicio_cuentas.obtener_cuenta(_id)
        if not cuenta:
            return jsonify(error="No se a encontrado ninguna cuenta!"), 404
        return jsonify(cuenta), 200
    if request.method == 'PUT' and request.is_json:
        cuenta = request.get_json()
        if not cuenta:
            return jsonify(error="No se ha recibido ninguna información para actualizar"), 400
        respuesta = servicio_cuentas.actualizar_cuenta(cuenta, _id)
        return respuesta
    if request.method == 'DELETE':
        cuenta = servicio_cuentas.eliminar_cuenta(_id)
        if cuenta:
            return jsonify("se a eliminado con exito la cuenta!"), 200
        else:
            return jsonify("no se a podido eliminar la cuenta con exito :C"), 400


@bp_cuentas.route("/cuentas/password/<_id>", methods=['POST'])
@login_required
def actualizar_password(_id):
    if request.method == 'POST' and request.is_json:
        datos = request.get_json()
        password = datos.get('password')
        new_password = datos.get('new_password')
        return servicio_cuentas.actualizar_password(_id, password, new_password)
