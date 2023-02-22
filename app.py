from flask import Flask, jsonify, url_for, redirect, request
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_swagger import swagger

from controladores.controlador_auth import bp_auth
from controladores.controlador_cuentas import bp_cuentas
from servicios.servicio_health import check_status
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600000
api = Api(app)
jwt = JWTManager(app)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Pinolabs Backend",
        'app_version': "1.0.3"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/api/swagger.json')
def swagger_api():
    swag = swagger(app)
    swag['info']['version'] = "1.0.3"
    swag['info']['title'] = "ApiFlask Backend"
    swag['info']['description'] = 'Este documento contiene la documentacion de esta api en formato OpenAPI'
    swag['host'] = request.host
    swag['paths'] = {"Authorization": '/api/auth/login', 'Gestion de Cuentas': '/api/cuentas'}
    return jsonify(swag)


app.register_blueprint(bp_auth)
app.register_blueprint(bp_cuentas)


@app.route('/')
def index():
    return redirect(url_for('api'))


@app.route('/api')
def api():
    return '<h1 style="text-align: center; margin-top: 50px;">Bienvenido al backend de pinolabs</h1>'


@app.route('/health', methods=['GET', 'POST'])
def health():
    status = check_status()
    return status


@app.errorhandler(405)
def not_allowed(error):
    return jsonify(message="Hey tu, ¿Que Estas Buscando?"), 405


@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify({"error": "No se ha ingresado un token valido"}), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify(Error="Pagina No Encontrada =("), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
