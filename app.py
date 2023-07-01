from flask import Flask, render_template ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/chatdb'
# URI de la BBDD driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
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




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat')
def chat():
    return render_template("chat.html")

@app.route('/loging')
def loging():
    return render_template("loging.html")

@app.route('/loging-form',methods=['POST'])
def login_form():
    data = request.form
    print(data)
    user = data['user']
    password = data['password']
    print(user)
    print(password)
    print(User.name.get(str(user)))
    return render_template("index.html")

 
@app.route('/singup')
def singup():
    return render_template("singup.html")

@app.route('/singup-form',methods=['POST'])
def singup_form():
    data = request.form
    print(data)
    user = data['user']
    password = data['password']
    print(user)
    print(password)
    new_user = User(user,password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('chat.html')

if __name__=='__main__':
    app.run(debug=True, port=5000)