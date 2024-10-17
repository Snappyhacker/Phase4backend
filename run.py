# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import bcrypt

# app = Flask(__name__)
# CORS(app, resources={r"/auth/*": {"origins": "http://localhost:3000"}})

# # In-memory user storage (replace with a database in production)
# users = {}


# @app.route('/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()

#     # Check if the user already exists
#     if data['email'] in users:
#         return jsonify({'message': 'User already exists'}), 409

#     # Hash the password
#     hashed_password = bcrypt.hashpw(
#         data['password'].encode('utf-8'), bcrypt.gensalt())

#     # Store the user details
#     users[data['email']] = {
#         'username': data['username'],
#         'password': hashed_password
#     }

#     return jsonify({'message': 'User registered successfully'}), 201


# @app.route('/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = users.get(data['email'])

#     if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
#         return jsonify({'username': user['username']}), 200

#     return jsonify({'message': 'Invalid credentials'}), 401

# if __name__ == '__main__':
#     app.run(debug=True)

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()
    # app.run(host='localhost', debug=True, port=5001)