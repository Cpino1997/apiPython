from flask import Flask,jsonify
app = Flask(__name__) 

@app.errorhandler(404)
def not_found(error):
    return jsonify(message="Endpoint no encontrado"), 404

@app.errorhandler(405)
def que_buscas(error):
    return jsonify(message="Hey tu!, que estas buscando?"), 405

@app.errorhandler(401)
def error_auth():
    return jsonify(mensaje="Error, debes ingresar a tu cuenta para ingresar aqui!"),401
