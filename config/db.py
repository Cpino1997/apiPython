import os
import pymysql


def obtener_conexion():
    return pymysql.connect(host=host,
                           user=user,
                           password=password,
                           db=db)


host = os.environ.get('DB_HOST', 'localhost')
user = os.environ.get('DB_USER', 'root')
password = os.environ.get('DB_PASSWORD', 'root')
db = os.environ.get('DB_NAME', 'app')
