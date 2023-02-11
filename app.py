from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask_restful import Resource, Api
from flask_session import Session

from app_utils.password_manager import hash_password, check_password
from config import ConfigClass

from models.User import User, Role, UserRole

app = Flask(__name__)
api = Api(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

if len(ConfigClass.DATABASE.get_tables()) == 0:
    ConfigClass.DATABASE.create_tables([User, Role, UserRole])
    ConfigClass.DATABASE.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['logged'] is None:
            return make_response(render_template('login_required.html'), 200)
        return f(*args, **kwargs)
    return decorated_function


class Home(Resource):
    def get(self):
        resp = make_response(render_template('index.html'), 200)
        return resp


class Users(Resource):
    @login_required
    def get(self):
        ConfigClass.DATABASE.connect()
        users = User.select()
        ConfigClass.DATABASE.close()
        user_list = []
        for user in users:
            user_list.append(user)
        resp = make_response(render_template('users.html', user_list=user_list), 200)
        return resp


class Register(Resource):
    def get(self, status=200, **kwargs):
        resp = make_response(render_template('register.html', **kwargs), status)
        return resp

    def post(self):
        data = request.form.to_dict()
        if User.filter(username=data["username"]).count() != 0:
            return self.get(status=400, error="Username is taken! Try with other one!")
        User.create(username=data["username"], password=hash_password(data["password"]))
        return redirect(url_for('home'))


class Login(Resource):
    def get(self, status=200, **kwargs):
        resp = make_response(render_template('login.html', **kwargs), status)
        return resp

    def post(self):
        data = request.form.to_dict()
        if data["username"] is None or data["password"] is None:
            return self.get(status=400, error="Enter both Login and password to login!")
        user = User.get_or_none(username=data['username'])
        if user:
            if check_password(user, data['password']):
                session["username"] = user.username
                session["logged"] = True
                return redirect(url_for('home'))
        else:
            return self.get(status=400, error="Wrong login or password!")


class Logout(Resource):
    def get(self):
        session["username"] = None
        session["logged"] = None
        return redirect(url_for('home'))


api.add_resource(Home, '/', '/home', '/index')
api.add_resource(Users, '/users')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run()
