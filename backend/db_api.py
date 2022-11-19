import peewee
from peewee import *

conn = SqliteDatabase('sovkombank_db')


class BaseModel(Model):
    class Meta:
        database = conn


class Role(BaseModel):
    role_id = AutoField(column_name='user_id')
    name_role = TextField(column_name='name_role', null=False)


class User(BaseModel):
    user_id = AutoField(primary_key=True, column_name='user_id', unique=True,
                        constraints=[peewee.SQL('AUTO_INCREMENT')])
    login = TextField(column_name='login', null=False)
    password = TextField(column_name='password', null=False)
    role_id = ForeignKeyField(Role, backref='users')

    class Meta:
        table_name = 'users'


cursor = conn.cursor()


def get_user_by_id(id):
    return User.get(User.user_id == id)

def get_user_by_login(login):
    return User.get(User.login == login)

def create_user(login, password, role):
    User.create(login=login, password=password, role_id=role)


def delete_user(id):
    User.delete().where(User.user_id == id).execute()


conn.close()
