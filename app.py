from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask (__name__)
#CONFIGURACION DE BDA SQL LITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Modelo de tabla
class log(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.Text)

#CREAR TABLA SI NO EXISTE
with app.app_context():
    db.create_all()

    prueba1 = log(texto='Mensaje de Prueba 1')
    prueba2 = log(texto='Mensaje de Prueba 2')
    db.session.add(prueba1)
    db.session.add(prueba2)
    db.session.commit()

#Funcion para ordenar x Fecha y Hora
def ordenerar_fyh(registros):
    return sorted(registros,key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')
def index():
    #obtener regrestros
    registros = log.query.all()
    registros_orde = ordenerar_fyh(registros)
    return render_template('index.html',registros=registros_orde)

mensajes_log = []

#funcion para save msm en bd
def agregar_mensajes_log(texto):
    mensajes_log.append(texto)

    #Gurdar en bd
    nuevo_registro = log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()

if __name__=='__main__':
    app.run(host='0.0.0.0',port= 80,debug=True)
