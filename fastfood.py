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
		return jsonify({"message" : "Try another username"})

#Login authorisation
def log_auth(username, password):
	if username in user:
		if password == user[username]['password']:
			return True
	return False

#check if user is in session
def check_user(func):
	@wraps(func)
	def wraps(*args, **kwargs):
		if session["check_user"]:
			return func(*args, *kwargs)
		else:
			return jsonify({'message' : "please login to continue"}), 401

#Login if registered
@app.route('/api/v1/login', methods=['POST'])
def login():
	username = request.get_json()['username']
	password = request.get_json()['password']
	if log_auth(username,password):
		return jsonify({'message' : 'welcome to Fast-Food-Fast'}), 200
	else:
		return jsonify({'message' : "invalid details"}), 401

@app.route('/api/v1/make_order', methods=['POST'])
def make_order():
	username = session.get("username")

	food = request.get_json()['food']
	quantity = request.get_json()['quantity']
	location = request.get_json()['location']

	if username not in orders:
		orders.update({username:[]})
	orders[username].append(food)
	orders[username].append(quantity)
	orders[username].append(location)

	return jsonify({"message": "You just made an order"})
#Initalization
if __name__=="__main__":
	app.run(debug = True,port=5004)