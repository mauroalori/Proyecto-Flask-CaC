from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://mauroalori:mauro12345@mauroalori$default/mauroalori.mysql.pythonanywhere-services.com'
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
    ciudad=db.Column(db.String(400))
    def __init__(self,nombre,apellido,tiempo,ciudad):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.tiempo=tiempo
        self.ciudad=ciudad


    #  si hay que crear mas tablas , se hace aqui


with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class CorredorSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','tiempo','ciudad')


corredor_schema=CorredorSchema()            # El objeto producto_schema es para traer un producto
corredores_schema=CorredorSchema(many=True)  # El objeto productos_schema es para traer multiples corredors de producto


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
    ciudad=request.json['ciudad']
    new_corredor=Corredor(nombre,apellido,tiempo,ciudad)
    db.session.add(new_corredor)
    db.session.commit()
    return corredor_schema.jsonify(new_corredor)

@app.route('/corredores/<id>' ,methods=['PUT'])
def update_corredor(id):
    corredor=Corredor.query.get(id)
 
    corredor.nombre=request.json['nombre']
    corredor.apellido=request.json['apellido']
    corredor.tiempo=request.json['tiempo']
    corredor.ciudad=request.json['ciudad']

    db.session.commit()
    return corredor_schema.jsonify(corredor)
 

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
