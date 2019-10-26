from flask import Flask, render_template, make_response, jsonify, request
import os
import time

app = Flask(__name__)

#def format_server_time():
#  server_time = time.localtime()
#  return time.strftime("%I:%M:%S %p", server_time)

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

@app.route('/customers', methods = ['POST'])
def create_customer():
  customer_to_create = request.get_json()

  return jsonify({
      'status': 'OK',
      'message': 'Customer created'
  })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
