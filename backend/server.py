import hashlib
import os
import datetime
import jwt
from flask_cors import CORS, cross_origin
import db_api
import base64
from functools import wraps
from typing import Optional
from flask import request, jsonify, make_response, Flask
from db_api import User


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
app.config['CORS_HEADERS'] = 'Content-Type'
salt = os.urandom(32)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


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
    user = list(db_api.get_user_by_login(login))
    if user.__len__() == 0:
        db_api.create_user(login, hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 10000, dklen=128), 0,
                           salt)
        response = make_response(
            jsonify(
                {
                    'userId': user[0].user_id,
                    'login': user[0].login,
                }
            ), 200
        )
        return response
    else:
        return 'user is already exist'


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = list(db_api.get_user_by_login(auth.username))
    if user.__len__() != 0:
        if check_password_hash(user[0], auth.password):
            token = jwt.encode(
                {'user_id': user[0].user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            response = make_response(jsonify({'token': token
                            # 'userId': user[0].user_id,
                            # 'login': user[0].login,
                            }), 200
                )
            response.headers["Content-Type"] = "application/json"
            return response
        else:
            response = make_response(
                jsonify(
                    {
                        'msg': 'login or password incorrect',
                    }
                ), 401
            )
            response.headers["Content-Type"] = "application/json"
            response.headers["WWW-Authenticate"] = "Basic realm=notes_api"
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
        response.headers["WWW-Authenticate"] = "Basic realm=notes_api"
        return response


## TODO удалять может только админ
'''
@app.route('/deleteUser')
@token_required
def delete_user():
    user_id = request.args.get('userId')
    db_api.delete_user(user_id)
    return 'user deleted'

@app.route('/getAccountsForUser')
@token_required
def delete_user():
    user_id = request.args.get('userId')
    db_api.delete_user(user_id)
    return 'user deleted'
'''

@app.route('/getUserById')
def get_user_by_id():
    user_id = request.args.get('userId')
    user = db_api.get_user_by_id(user_id)
    return str(user.user_id)


def identify_user() -> Optional[User]:
    scheme, credentials = request.headers.get('Authorization').split()
    if not credentials:
        return None

    decoded_credentials = base64.b64decode(credentials).decode()
    username, _ = decoded_credentials.split(':')

    user = User.query.filter_by(username=username).first()

    return user

def check_password_hash(user, auth_password):
    if user.password == hashlib.pbkdf2_hmac('sha256', auth_password.encode('utf-8'), user.salt, 10000, dklen=128):
        return True
    else:
        return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)
