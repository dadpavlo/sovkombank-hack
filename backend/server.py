from uuid import uuid4

from flask import Flask, make_response, jsonify
from flask import request
import db_api

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return 'Hello World'


@app.route('/signUp', methods=['POST'])
def signup_post():
    login = request.args.get('login')
    password = request.args.get('password')
    user = db_api.get_user_by_login(login)
    if user is None:
        db_api.create_user(login, password, 0)
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
            response = make_response(
                jsonify(
                    {
                        'msg': 'login',
                    }
                ), 200
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
