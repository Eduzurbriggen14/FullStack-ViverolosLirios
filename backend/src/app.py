from flask import Flask ,jsonify ,request
from flask_cors import CORS   
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend


# configuro la base de datos, con el nombre el usuario y la clave
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://LuisEscobar:vivero123@LuisEscobar.mysql.pythonanywhere-services.com/LuisEscobar$lirios'
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://eduz14:MyNewPass@eduz14.mysql.pythonanywhere-services.com/eduz14$losliriosBD'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:MyNewPass@localhost/vivero'
# URI de la BBDD driver de la BD  user:clave@URLBBDD/nombreBBDD

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
app.config['JWT_SECRET_KEY']= '123456789'

db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow
jwt= JWTManager(app)



# modelos/ definimos las tablas de la base de datos con sus atributos

class Producto(db.Model):
    codigo=db.Column(db.Integer, primary_key=True, autoincrement=True )   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    descripcion=db.Column(db.String(200))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    categoria=db.Column(db.Enum('lirios','frutales','herramientas'))
    imagen=db.Column(db.String(400))

    def __init__(self,nombre,descripcion,precio,stock,categoria,imagen):  
        self.nombre=nombre   
        self.descripcion=descripcion
        self.precio=precio
        self.stock=stock
        self.categoria=categoria
        self.imagen=imagen
   
class Usuario(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario= db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(15), nullable=False)
    nombreCompleto=db.Column(db.String(100), nullable=True)
    es_administrador = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)

    def __init__(self,usuario, password, nombreCompleto, es_administrador, activo):
        self.usuario= usuario
        self.password= password
        self.nombreCompleto= nombreCompleto
        self.es_administrador= es_administrador
        self.activo = activo
        


with app.app_context(): 
    db.create_all()  # crea la BD


#definimos como se muestran los datos en la tabla
class ProductoSchema(ma.Schema): 
    class Meta:
        fields=('codigo','nombre','descripcion','precio','stock','categoria','imagen')

producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto, creamos una instancia
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

class UsuarioSchema(ma.Schema):
    class Meta:
        fields= ('id','usuario','nombreCompleto', 'es_administrador','activo',)

usuario_schema=UsuarioSchema()
usuarios_schema=UsuarioSchema(many=True)


#Creamos las urls de productos----------------------------------------------------------------

@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos = Producto.query.all()         
    result = productos_schema.dump(all_productos) 
                                                 
    return jsonify(result)                       




@app.route('/producto/<codigo>',methods=['GET'])
def get_producto(codigo):
    producto=Producto.query.get(codigo)
    return producto_schema.jsonify(producto)   




@app.route('/delete/<codigo>',methods=['DELETE'])
def delete_producto(codigo):
    producto=Producto.query.get(codigo)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)  


@app.route('/producto', methods=['POST']) 
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente con los valores para cada variable
    nombre=request.json['nombre']
    descripcion=request.json['descripcion']
    precio=request.json['precio']
    stock=request.json['stock']
    categoria=request.json['categoria']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,descripcion,precio,stock,categoria,imagen) #se crea una instancia de un nuevo producto
    db.session.add(new_producto)#agregamos el producto
    db.session.commit()#confirmamos
    return producto_schema.jsonify(new_producto)


@app.route('/update/<codigo>' ,methods=['PUT'])
def update_producto(codigo):
    producto=Producto.query.get(codigo)  #obtenemos un producto mediante su codigo

    #actualizamos los atributos del objeto producto con los valores proporcionados por el json que se recibe en la solicitud
    producto.nombre=request.json['nombre']
    producto.descripcion=request.json['descripcion']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.categoria=request.json['categoria']
    producto.imagen=request.json['imagen']

    db.session.commit()
    return producto_schema.jsonify(producto)



#Creamos las urls de usuarios----------------------------------------------------------------

@app.route("/usuario", methods=["POST"])
def crete_user():
    usuario= request.json['usuario']
    password= request.json['password']
    nombreCompleto= request.json['nombreCompleto']
    es_administrador= request.json.get('es_administrador', False)
    activo= request.json.get('activo', True)


    nuevo_usuario= Usuario(usuario, password, nombreCompleto, es_administrador, activo)
    
    db.session.add(nuevo_usuario)
    db.session.commit()

    return usuario_schema.jsonify(nuevo_usuario)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('usuario')
    password = request.form.get('password')

    print(username)
    print(password)

    if username is not None and password is not None:
        user = Usuario.query.filter_by(usuario=username, password=password, activo=True).first()
        print(user)

        if user:
            additional_claims = {"es_administrador": user.es_administrador}
            access_token = create_access_token(identity=user.usuario, additional_claims=additional_claims)
            print(access_token)
            return jsonify(access_token=access_token, es_administrador=user.es_administrador, username= username), 200
        else:
            return jsonify(mensaje="Credenciales inválidas, ingrese sus datos nuevamente."), 401
    else:
        return jsonify(mensaje="Complete todos los campos")
    

@app.route("/get_info", methods=["POST"])
@jwt_required()
def get_info():
    # Obtener la identidad (username) y las reclamaciones (claims) del token de acceso
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify({"usuario": current_user, "es_administrador": claims["es_administrador"]}), 200



# programa principal *******************************
if __name__=='__main__':
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000

    #debug=true nos permite poder inspeccionar los errores
