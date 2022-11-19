import hashlib
import os
from uuid import uuid4

from flask import Flask, make_response, jsonify
from flask import request
import db_api

import base64
from functools import wraps
from typing import Optional

from flask import request, jsonify, make_response

# import services as notes_service
# from app import app
from db_api import User
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
salt = os.urandom(32)

@app.route('/')
def index():
    return 'Hello World'



# def authenticated_only(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         user = identify_user()
#
#         scheme, credentials = request.headers.get('Authorization').split()
#         decoded_credentials = base64.b64decode(credentials).decode()
#         username, password = decoded_credentials.split(':')
#
#         is_authenticated = authenticate_user(user=user, password=password)
#
#     # Not authenticated users not authorized to do this action
#         if not is_authenticated:
#             response = make_response(
#                 jsonify(
#                     {
#                         'msg': 'Credentials not valid',
#                     }
#                 ), 401
#             )
#             response.headers["Content-Type"] = "application/json"
#             response.headers["WWW-Authenticate"] = "Basic realm=notes_api"
#
#             return response
#
#         request.user = user
#
#         return f(*args, **kwargs)
#     return wrapper

@app.route("/notes", methods=['POST'])
def create_note():

    response = make_response(
        jsonify(
            {
                'title': 'note.title',
                'body': 'note.body',
            }
        ), 201
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/signUp', methods=['POST'])
def signup_post():
    login = request.args.get('login')
    password = request.args.get('password')
    user = db_api.get_user_by_login(login).count
    if user == 0:
        db_api.create_user(login, hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 10000), 0)
        return 'created user'
    else:
        return 'user is already exist'

@app.route('/login')
def sign_up():
    login = request.args.get('login')
    password = request.args.get('password')
    user = db_api.get_user_by_login(login)
    if user is not None:
        if user.password == password:
            return 'login'
        else:
            response = make_response(
                jsonify(
                    {
                        'msg': 'Credentials not valid',
                    }
                ), 401
            )
            response.headers["Content-Type"] = "application/json"
            return response
    else:
        response = make_response(
            jsonify(
                {
                    'msg': 'Credentials not valid',
                }
            ), 401
        )
        response.headers["Content-Type"] = "application/json"
        return response

## TODO удалять может только админ
@app.route('/deleteUser')
def delete_user():
    user_id = request.args.get('userId')
    db_api.delete_user(user_id)
    return 'user deleted'


@app.route('/getUserById')
def get_user_by_id():
    user_id = request.args.get('userId')
    user = db_api.get_user_by_id(user_id)
    return str(user.user_id)

def authenticate_user(user: Optional[User], password: str) -> bool:
    if user is None:
        return False

    return user.password == PasswordHash.hash_password(password)


def identify_user() -> Optional[User]:
    scheme, credentials = request.headers.get('Authorization').split()
    if not credentials:
        return None

    decoded_credentials = base64.b64decode(credentials).decode()
    username, _ = decoded_credentials.split(':')

    user = User.query.filter_by(username=username).first()

    return user


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
