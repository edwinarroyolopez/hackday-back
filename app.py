from flask import Flask, render_template, make_response, jsonify, request
import os
import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

#Local
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:halo4g2hp@localhost:3306/myboard'
db = SQLAlchemy(app)

#PDN
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rockets:jksjdfksdjf847545hHT*@rockets.mysql.pythonanywhere-services.com:3306/rockets$mydatabase'
#db = SQLAlchemy(app)

#def format_server_time():
#  server_time = time.localtime()
#  return time.strftime("%I:%M:%S %p", server_time)

def send_email_to_verify(data):
    body = '''
    <html>

    <body>
    <div align="center">
    <div align="center" style="padding: 50px; border: 1px solid #ccc; width: 30%">
    <p>Hi Mr(s)''' + data['name'] + ''', </p>
    <p>Attached is the link to verify your identity</p>
    <a href="http://rockets.pythonanywhere.com/customers/''' + data['customer_id'] + '''/verify">Verify your identity</a>
    </div>
    </div>
    </body>

    </html>
    '''

    url = 'https://hook.integromat.com/lboq8sa4cxjkvfck8hhx7fsay1pq3sxo'

    headers = {
        'X-SECURITY-TOKEN': '12345'
    }

    data = {
        'to': data['to'],
        'subject' : 'Please verify your identity',
        'body': body
    }

    #response = requests.post(url, data=data,files=files, headers=headers)
    response = requests.post(url, data=data, headers=headers)

@app.route('/')
def index():
    #context = { 'server_time': format_server_time() }
    #return render_template('index.html', context=context)
    return 'Hola desde index'

@app.route('/customers', methods = ['GET'])
def get_customers():
  customers = [
    {
      'id': 1,
      'name': 'Francisco',
      'cellphone': '3000000000',
      'email': 'email@mail.com'
    },
    {
      'id': 2,
      'name': 'Edwin',
      'cellphone': '3010000000',
      'email': 'email@mail.ru'
    }
  ]

  return jsonify(customers)

@app.route('/sendtermsandconditions', methods = ['POST'])
def send_terms_and_conditions():
  customer_to_create = request.get_json()

  return jsonify({
      'status': 'OK',
      'message': 'Terms and conditions sent'
  })

@app.route('/acepttermsandconditions', methods = ['GET'])
def acept_terms_and_conditions():
  contract_id = request.args.get('contract')

  contract_info = {}

  return render_template('terms-and-conditions-acepted.html', context=contract_info)

#Create a customer
@app.route('/customers', methods = ['POST'])
def create_customer():
  data_input = request.get_json()

  customer = Customer(
    name   = data_input['name'],
    cellphone = data_input['cellphone'],
    dni = data_input['dni'],
    email   = data_input['email'],
    gender    = data_input['gender'],
    date_birth    =  data_input['date_birth'],
    isVerify = 1
  )

  save_item_to_db(customer)

  #Consultar con el email del seller
  #email_seller = data_input['email_seller']
  id_seller = 1

  contract = Contract(
    name = data_input['name'],
    idSeller = id_seller,
    idClient = customer.id
  )

  save_item_to_db(contract)

  # TODO: Enviar correo con link para aceptar terminos y condiciones
  
  send_email_to_verify({
      'to': data_input['email'],
      'name': data_input['name'],
      'customer_id': customer.id
  })

  return jsonify({
      'status': 'OK',
      'message': 'Customer created',
      'idClient': customer.id,
      'idContract': contract.id
  })


@app.route('/dashboard', methods = ['GET'])
def dashboard():
  return render_template('dashboard.html')

@app.route('/contract', methods = ['GET'])
def contract():
  return render_template('contract.html')

class Seller(db.Model):
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cellphone = db.Column(db.String(200), nullable=True)
    #dni = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Seller %r>' % self.name

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cellphone = db.Column(db.String(200), nullable=True)
    dni = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    gender = db.Column(db.String(200), nullable=True)
    date_birth = db.Column(db.DateTime(), nullable=True)
    isVerify = db.Column(db.Integer, nullable=False, default=1)
    idSeller = db.Column(db.Integer)

    def __repr__(self):
        return '<Customer %r>' % self.name

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    idSeller = db.Column(db.Integer)
    idClient = db.Column(db.Integer)

    def __repr__(self):
        return '<Contract %r>' % self.name

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    url = db.Column(db.String(200), nullable=True)
    idSeller = db.Column(db.Integer)
    idCustomer = db.Column(db.Integer)

    def __repr__(self):
        return '<Document %r>' % self.name

#Save to BD
def save_item_to_db(item_to_save):
    db.session.add(item_to_save)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
