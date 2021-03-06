from flask import Flask, jsonify, request, session
from functools import wraps

app = Flask(__name__)


app.config['SECRET_KEY'] = "philipotieno"
user = {}
orders = {}


#Homepage route
@app.route('/api/v1/', methods=['GET'])
def home():
	return jsonify({'message' : 'welcome to Fast-Food-Fast'}), 200


#Register new user
@app.route('/api/v1/register', methods=['POST'])
def register():
	name = request.get_json()['name']
	username = request.get_json()['username']
	email = request.get_json()['email']
	password = request.get_json()['password']

	if username not in user:
		user.update({username:{"name":name, "email":email, "password":password}})
		return jsonify(user), 200

	else:
		return jsonify({"message" : "User already registered"})

#Login authorisation
def log_auth(username, password):
	if username in user:
		if password == user[username]['password']:
			return True
	return False

#check if user is in session
def check_user(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		if session["check_user"]:
			return func(*args, **kwargs)
		else:
			return jsonify({'message' : "please login to continue"}), 401

	return wrap

#Login if registered
@app.route('/api/v1/login', methods=['POST'])
def login():
	username = request.get_json()['username']
	password = request.get_json()['password']
	if log_auth(username,password):
		session['check_user'] = True
		session['username'] = username
		return jsonify({'message' : 'welcome to Fast-Food-Fast'}), 200
	else:
		return jsonify({'message' : "invalid details"}), 401

#make an order
@app.route('/api/v1/make_order', methods=['POST'])
@check_user
def make_order():
	username = session.get("username")

	food = request.get_json()['food']

	if username not in orders:
		orders.update({username:[]})
	orders[username].append(food)
	return jsonify({"message" : "Order sent"}), 200

@app.route('/api/v1/history', methods=['GET'])
@check_user
def history():
	username = session.get('username')
	my_history = {}
	for each in orders[username]:
		my_history.update({orders[username].index(each) + 1:each})
	return jsonify(my_history), 200

@app.route('/api/v1/fetch/<int:order_id>', methods=['GET'])
@check_user
def fetch(order_id):
	username =  session.get('username')
	return jsonify({order_id:orders[username][order_id-1]}), 200

#A function that updates the orders and maintains the index position
def update(old_order, new_order, mlo):
	for i in mlo:
		if i == old_order:
			index = mlo.index(i)
			del mlo[index]
			mlo.insert(index, new_order)

#Update an existing food order	
@app.route('/api/v1/update_order/<int:order_id>', methods=['PUT'])
@check_user
def update_order(order_id):
	food = request.get_json()['food']
	username = session.get('username')
	old_order = orders[username][order_id-1]
	update(old_order, food, orders[username])
	return jsonify({'message' : 'order updated successfully'}), 200


@app.route('/api/v1/delete_order/<int:order_id>', methods=['DELETE'])
@check_user
def delete_order(order_id):
	username = session.get('username')
	del orders[username][order_id]
	return jsonify({'message' : 'successfully deleted order'}), 200

#Initalization
if __name__=="__main__":
	app.run(debug = True,port=5012)

