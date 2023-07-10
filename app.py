from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://mauroalori:mauro12345@mauroalori.mysql.pythonanywhere-services.com/mauroalori$default'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Corredor(db.Model):   # la clase Producto hereda de db.Model
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    tiempo=db.Column(db.Time)
    pais=db.Column(db.String(400),db.ForeignKey('pais.codigo'))
    def __init__(self,nombre,apellido,tiempo,pais):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.tiempo=tiempo
        self.pais=pais

class Pais(db.Model):
    codigo=db.Column(db.String(400), primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    imagen=db.Column(db.String(400))
    def __init__(self,codigo,nombre,imagen):   #crea el  constructor de la clase
        self.codigo=codigo
        self.nombre=nombre
        self.imagen=imagen
    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class CorredorSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','tiempo','pais')

class PaisSchema(ma.Schema):
    class Meta:
        fields=('codigo','nombre','imagen')

corredor_schema=CorredorSchema()            # El objeto corredor_schema es para traer un corredor
corredores_schema=CorredorSchema(many=True)  # El objeto corredores_schema es para traer multiples corredores

pais_schema=PaisSchema()            # El objeto pais_schema es para traer un pais
paises_schema=PaisSchema(many=True)  # El objeto paises_schema es para traer multiples paises

# crea los endpoint o rutas (json)
@app.route('/corredores',methods=['GET'])
def get_Corredores():
    all_corredores=Corredor.query.all()         # el metodo query.all() lo hereda de db.Model
    result=corredores_schema.dump(all_corredores)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los corredors de la tabla
    return jsonify(result)                       # retorna un JSON de todos los corredors de la tabla


@app.route('/corredores/<id>',methods=['GET'])
def get_corredor(id):
    corredor=Corredor.query.get(id)
    return corredor_schema.jsonify(corredor)   # retorna el JSON de un producto recibido como parametro


@app.route('/corredores/<id>',methods=['DELETE'])
def delete_corredores(id):
    corredor=Corredor.query.get(id)
    db.session.delete(corredor)
    db.session.commit()
    return corredor_schema.jsonify(corredor)   # me devuelve un json con el corredor eliminado

@app.route('/corredores', methods=['POST']) # crea ruta o endpoint
def create_corredor():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    tiempo=request.json['tiempo']
    pais=request.json['pais']
    new_corredor=Corredor(nombre,apellido,tiempo,pais)
    db.session.add(new_corredor)
    db.session.commit()
    return corredor_schema.jsonify(new_corredor)

@app.route('/corredores/<id>' ,methods=['PUT'])
def update_corredor(id):
    corredor=Corredor.query.get(id)

    corredor.nombre=request.json['nombre']
    corredor.apellido=request.json['apellido']
    corredor.tiempo=request.json['tiempo']
    corredor.pais=request.json['pais']

    db.session.commit()
    return corredor_schema.jsonify(corredor)

#endpoints para los paises
@app.route('/paises',methods=['GET'])
def get_Paises():
    all_paises=Pais.query.all()         # el metodo query.all() lo hereda de db.Model
    result=paises_schema.dump(all_paises)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los paiss de la tabla
    return jsonify(result)                       # retorna un JSON de todos los paiss de la tabla

@app.route('/paises/<codigo>',methods=['GET'])
def get_pais(codigo):
    pais=Pais.query.get(codigo)
    return pais_schema.jsonify(pais)   # retorna el JSON de un producto recibido como parametro

@app.route('/paises/<codigo>',methods=['DELETE'])
def delete_paises(codigo):
    pais=Pais.query.get(codigo)
    db.session.delete(pais)
    db.session.commit()
    return pais_schema.jsonify(pais)   # me devuelve un json con el pais eliminado

@app.route('/paises', methods=['POST']) # crea ruta o endpoint
def create_pais():
    #print(request.json)  # request.json contiene el json que envio el cliente
    codigo=request.json['codigo']
    nombre=request.json['nombre']
    imagen=request.json['imagen']
    new_pais=Pais(codigo,nombre,imagen)
    db.session.add(new_pais)
    db.session.commit()
    return pais_schema.jsonify(new_pais)

@app.route('/paises/<codigo>' ,methods=['PUT'])
def update_pais(codigo):
    pais=Pais.query.get(codigo)

    pais.codigo=request.json['codigo']
    pais.nombre=request.json['nombre']
    pais.imagen=request.json['imagen']

    db.session.commit()
    return pais_schema.jsonify(pais)

# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
