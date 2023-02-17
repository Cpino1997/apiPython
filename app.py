from flask import Flask, jsonify, url_for, redirect
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from controladores.controlador_auth import bp_auth
from controladores.controlador_cuentas import bp_cuentas
from servicios.servicio_health import check_status

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
api = Api(app)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(bp_auth)
app.register_blueprint(bp_cuentas)


@app.route('/')
def index():
    return redirect(url_for('api'))


@app.route('/api')
def api():
    return '<h1>Bienvenido al backend de pinolabs</h1>'


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
