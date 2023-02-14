from flask import Flask, jsonify
from flask_cors import CORS

from controladores.validadores import validadores
from controladores.controlador_auth import bp_auth
from controladores.controlador_cuentas import bp_cuentas
from servicios.servicio_health import check_status

app = Flask(__name__)
app.secret_key = 'holakeHace'
CORS(app)

app.register_blueprint(bp_cuentas)
app.register_blueprint(bp_auth)
app.register_blueprint(validadores)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    header['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    header['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


@app.route('/health', methods=['GET', 'POST'])
def health():
    status = check_status()
    return status


@app.errorhandler(405)
def not_allowed(error):
    return jsonify(message="Que Estas Buscando? o.O"), 405


@app.errorhandler(404)
def not_found(error):
    return jsonify(Error="Pagina No Encontrada =("), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
