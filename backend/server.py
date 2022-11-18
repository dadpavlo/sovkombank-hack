from uuid import uuid4

from flask import Flask
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
    else


    return 'created user'

@app.route('/login')
def sign_up():
    login = request.args.get('login')
    password = request.args.get('password')
    user = db_api.get_user_by_login(login)
    if user is not None:
        if user.password == password:
            rand_token = uuid4()

    return 'created user'

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
