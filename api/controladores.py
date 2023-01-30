from flask import Flask, jsonify, session, request
from config.db import Config
from flask_mysqldb import MySQL
from api.handlers import *

app = Flask(__name__) 
app.secret_key = 'holakeHace'

app.config.from_object(Config)
mysql = MySQL(app)

def apiLoginGet():
    estado = session.get('loggedin')
    if estado:
        cuenta = session['usuario']
        return jsonify(mensaje='Estas ingresado como '+ cuenta)
    else:
        return error_auth()

def apiLogin():
    if request.is_json:
        data = request.get_json()
        usuario = data.get('usuario')
        password = data.get('password')
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND password = %s', (usuario, password,))
        cuenta = cursor.fetchone()
    if cuenta:
        app.logger.info('%s Ha ingresado el usuario: ', usuario)
        session['loggedin'] = True
        session['id'] = cuenta['id']
        session['usuario'] = cuenta['usuario']
        return jsonify(success=True, mensaje='Inicio de sesión exitoso', usuario=cuenta)
    else:
        return jsonify(success=False, mensaje='Usuario o contraseña incorrecta')


def test22():                                      
   return jsonify({"mensaje":"Soy una prueba :v"})

def api_logout():                                     
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   return jsonify({"mensaje":"Session eliminada con exito!"})