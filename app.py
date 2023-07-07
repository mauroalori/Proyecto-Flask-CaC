from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@127.0.0.1/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Registro(db.Model):   # la clase Producto hereda de db.Model    
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
class RegistroSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','tiempo','ciudad')


registro_schema=RegistroSchema()            # El objeto producto_schema es para traer un producto
registros_schema=RegistroSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto


# crea los endpoint o rutas (json)
@app.route('/registros',methods=['GET'])
def get_Registros():
    all_registros=Registros.query.all()         # el metodo query.all() lo hereda de db.Model
    result=registros_schema.dump(all_registros)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/registros/<id>',methods=['GET'])
def get_registro(id):
    registro=Registro.query.get(id)
    return registro_schema.jsonify(registro)   # retorna el JSON de un producto recibido como parametro


@app.route('/registros/<id>',methods=['DELETE'])
def delete_registro(id):
    registro=Registro.query.get(id)
    db.session.delete(registro)
    db.session.commit()
    return registro_schema.jsonify(registro)   # me devuelve un json con el registro eliminado

@app.route('/registros', methods=['POST']) # crea ruta o endpoint
def create_registro():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    tiempo=request.json['tiempo']
    ciudad=request.json['ciudad']
    new_registro=Registro(nombre,apellido,tiempo,ciudad)
    db.session.add(new_registro)
    db.session.commit()
    return registro_schema.jsonify(new_registro)

@app.route('/registros/<id>' ,methods=['PUT'])
def update_registro(id):
    registro=Registro.query.get(id)
 
    registro.nombre=request.json['nombre']
    registro.apellido=request.json['apellido']
    registro.tiempo=request.json['tiempo']
    registro.ciudad=request.json['ciudad']

    db.session.commit()
    return registro_schema.jsonify(registro)
 

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
