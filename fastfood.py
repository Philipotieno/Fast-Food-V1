from flask import Flask, jsonify, request

app = Flask(__name__)


app.config['SECRET_KEY'] = "philipotieno"
user = {}

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
#Login authorisation
def log_auth(username, password):
	if username in user:
		if password == user[username]['password']:
			return True
	return False

#Login if registered
@app.route('/api/v1/login', methods=['POST'])
def login():
	username = request.get_json()['username']
	password = request.get_json()['password']
	if log_auth(username,password):
		return jsonify({'messge' : 'welcome to Fast-Food-Fast'})
	else:
		return jsonify({'messge' : 'invalid details'})
#Initalization
if __name__=="__main__":
	app.run(debug = True,port=5001)