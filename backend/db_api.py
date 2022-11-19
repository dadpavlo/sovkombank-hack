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
    password = BlobField(column_name='password', null=False)
    role_id = ForeignKeyField(Role, backref='users'),
    salt = BlobField(column_name='salt')
    class Meta:
        table_name = 'users'

class Account(BaseModel):
    account_id = IntegerField(primary_key=True, column_name='account_id', unique=True,
                        constraints=[peewee.SQL('AUTO_INCREMENT')])
    type = IntegerField(column_name='type')
    remains = IntegerField(column_name='remains')
    status = IntegerField(column_name='status')
    user_id = ForeignKeyField(User, backref="accounts")
    class Meta:
        table_name = 'accounts'
cursor = conn.cursor()

class Operation(BaseModel):
    operation_id = IntegerField(primary_key=True, column_name='operation_id', unique=True,
                        constraints=[peewee.SQL('AUTO_INCREMENT')])
    amount = IntegerField(column_name='amount')
    account_id = ForeignKeyField(Account, backref="operations")
    time = IntegerField(column_name='time') # unix timestamp in secs
    type = IntegerField(column_name='type') # 0-списание, 1- пополнение
    
    class Meta:
        table_name = 'operations'    

# actions with user
def get_user_by_id(id):
    return User.get(User.user_id == id)

def get_user_by_login(login):
    return User.select().where(User.login == login).execute()

def create_user(login, password, role, salt):
    User.create(login=login, password=password, role_id=role, salt = salt).save()
    print(User.login)


def delete_user(id):
    User.delete().where(User.user_id == id).execute()

# actions with account
def create_account(type,remains,status, user_ID):
    Account.create(type=type,remain = remains, status=status,user_id=user_ID).save()
    print(Account.remains)

def delelte_account(id):
    Account.delete().where(Account.user_id==id).execute()

def add_cash(id, amount, time):   
    Account.update({Account.remains : amount}).where(Account.account_id ==id).execute()
    create_operation(amount = amount, account_id=id, time=time, type= 1) 

def sub_cash(id, amount, time):
    Account.update({Account.remains : amount}).where(Account.account_id ==id).execute()
    create_operation(amount = amount, account_id=id, time=time, type= 0) 

#opertions actions
def create_operation( amount, account_id, time, type):
    Operation.create(amount =amount, account_id=account_id, time= time, type= type).save()

def delete_operation( id):
    Operation.delete().where(operation_id = id).execute()


create_user('Wildelm1914', 'qwerty', 0, 35)
create_account(0,10000.0,1,0)
print(add_cash(0,10001.0,1620000000))
print(sub_cash(0,100,1620000000))


#print(list(get_user_by_login('Wildelm1914')))
conn.close()
