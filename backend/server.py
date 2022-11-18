from flask import Flask
from flask import request
import db_api

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return 'Hello World'


@app.route('/signUp')
def sign_up():
    login = request.args.get('login')
    password = request.args.get('password')
    db_api.create_user(login, password, 0)
    return 'created user'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
