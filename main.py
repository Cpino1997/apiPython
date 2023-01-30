from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from dotenv import load_dotenv
from api.handlers import *
from config.db import * 
from api.controladores import *

load_dotenv()
app = Flask(__name__) 
app.secret_key = 'holakeHace'

app.config.from_object(Config)
mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            return jsonify(message='Debe iniciar sesión para acceder a este recurso'), 401
    return wrap

######Controladores de la app

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Mensaje para enviar cualquier respuesta
    msg = ''
    # Check usuario y password
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form:
        #Guardamos los datos del form en variables
        usuario = request.form['usuario']
        password = request.form['password']
        # Chekeamos si existe el usuario y la pwd en la bd
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s AND password = %s', (usuario, password,))
        account = cursor.fetchone()
        # Si el usuario existe agregamos los datos a nuestra session sino mandamos un error
        if account:
            app.logger.info('%s Ha ingresado el usuario: ', usuario)
            session['loggedin'] = True
            session['id'] = account['id']
            session['usuario'] = account['usuario']
            return redirect(url_for('home'))
        else:
            msg = 'Contraseña o Usuario incorrecto!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Removemos la session                                      
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usuario', None)
   return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    msg = ''
    if request.method == 'POST' and 'usuario' in request.form and 'password' in request.form and 'correo' in request.form:
        usuario = request.form['usuario']
        password = request.form['password']
        correo = request.form['correo']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE usuario = %s', (usuario,))
        account = cursor.fetchone()

        if account:
            msg = 'Este usuario ya se encuentra registrado!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
            msg = 'Direccion de correo invalida!'
        elif not re.match(r'[A-Za-z0-9]+', usuario):
            msg = 'El usuario solo puede tener letras y numeros!'
        elif not usuario or not password or not correo:
            msg = 'Porfavor Ingresa datos en el formulario!'
        else:
            cursor.execute('INSERT INTO cuentas VALUES (NULL, %s, %s, %s)', (usuario, password, correo,))
            mysql.connection.commit()
            msg = 'Te has registrado con exito!'
    elif request.method == 'POST':
        msg = 'Porfavor Ingresa datos en el formulario!'

    return render_template('registro.html', msg=msg)

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/perfil')
def perfil():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuentas WHERE id = %s', (session['id'],))
        cuenta = cursor.fetchone()
        return render_template('perfil.html', cuenta=cuenta)
    return redirect(url_for('login'))

@app.route('/recursos')
@login_required
def getRecursos():
    return jsonify(mensaje="Soy un recurso web")

### api points
app.add_url_rule('/api/test','test22',test22)
app.add_url_rule('/api/login', 'apiLogin', apiLogin, methods=['POST'])
app.add_url_rule('/api/login', 'apiLoginGet', apiLoginGet, methods=['GET'])
app.add_url_rule('/api/logout', 'api_logout', api_logout)

##### HealthCheck
health_status = True

@app.route('/toggle')
def toggle():
    global health_status
    health_status = not health_status
    return jsonify(health_value=health_status)

@app.route('/healthcheck')
def health():
    if health_status:
        resp = jsonify(health="vivo")
        resp.status_code = 200
    else:
        resp = jsonify(health="muerto")
        resp.status_code = 500
    return resp
 
if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"),host='0.0.0.0', port=os.getenv("PORT", default=5000))