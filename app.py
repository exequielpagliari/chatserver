from flask import Flask, render_template ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_socketio import send, emit
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Mariela@localhost:3308/chatdb'
# URI de la BBDD driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading', transports=['websocket'])
socketio = SocketIO(app)
db= SQLAlchemy(app) #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app) #crea el objeto ma de de la clase Marshmallow

class User(db.Model): # la clase Producto hereda de db.Model
    id=db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    name=db.Column(db.String(100))
    password=db.Column(db.String(100))
    def __init__(self,name,password): #crea el constructor de la clase
        self.name=name # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.password=password

class Chat(db.Model): # la clase Producto hereda de db.Model
    id=db.Column(db.Integer, primary_key=True) #define los campos de la tabla
    menssage=db.Column(db.String(100))
    user=db.Column(db.String(100))
    def __init__(self,menssage,user): #crea el constructor de la clase
        self.menssage=menssage # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.user=user


with app.app_context():
    db.create_all() # aqui crea todas las tablas

class ChatSchema(ma.Schema):
    class Meta:
        fields=('id','menssage','user')

chat_schema=ChatSchema() # El objeto producto_schema es para traer un producto
chats_schema=ChatSchema(many=True) # El objeto productos_schema es para traer multiples registros de producto

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','name','password')

user_schema=ChatSchema() # El objeto producto_schema es para traer un producto
users_schema=ChatSchema(many=True) # El objeto productos_schema es para traer multiples registros de producto

user_log_ok = None


@app.route('/')
def index():
    return render_template("index.html")



@app.route('/loging')
def loging():
    return render_template("loging.html",status='Ingrese el usuario')

@app.route('/loging-form',methods=['POST'])
def login_form(status=None):
    data = request.form
    user = data['user']
    password = data['password']
    user_log = User.query.filter_by(name=user).first()
    if user_log == None:
        print('No hay usuario')
        return render_template("loging.html",status='No existe el usuario')
    else:
        if user_log.password == password:
            user_log_ok = user_log
            print('Usuario Loggeado')
            return render_template("/chat.html")
        else:
            print('Error de Password')
            return render_template("loging.html",status='Error de Password')



 
@app.route('/singup')
def singup():
    return render_template("singup.html",status='Elija nombre de su perfil y contraseña')

@app.route('/singup-form',methods=['POST'])
def singup_form(status=None):
    data = request.form
    print(data)
    user = data['user']
    password = data['password']
    user_log = User.query.filter_by(name=user).first()
    if user_log == None:
        new_user = User(user,password)
        db.session.add(new_user)
        db.session.commit()
        user_log_ok = new_user
        return render_template('chat.html')
    else:
        return render_template('singup.html',status='Usuario ya registrado')
    

@app.route('/chat')
def chat():
    print(user_log_ok)
    return "chat.html"

@socketio.on('my event')
def handle_message(data=None,user_name=None,message=None):
    print(data)


@socketio.on('message')
def handle_message(user_name=None,message=None):
    print(user_name)


if __name__=='__main__':
    socketio.run(app)
    app.run(debug=True, port=5000)