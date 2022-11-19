import sqlite3

# def create_roles(db_name : str):
#     with sqlite3.connect(db_name) as db:
#         cursor = db.cursor()
#         query = """
#                     CREATE TABLE IF NOT EXISTS roles(
#                     role_id	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     name_role	TEXT
#                     );"""
#         print(query)
#         cursor.execute(query)
#         db.commit()
#
# def create_users(db_name : str):
#     with sqlite3.connect(db_name) as db:
#         cursor = db.cursor()
#         query = """
#                     CREATE TABLE IF NOT EXISTS users(
#                     user_id	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                     login	TEXT ,
#                     password	BLOB,
#                     salt BLOB,
#                     role_id	INTEGER,
#                     FOREIGN KEY(role_id) REFERENCES roles(role_id)
#                     );"""
#         print(query)
#         cursor.execute(query)
#         db.commit()

def create_accounts(db_name:str):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        query = """
                CREATE TABLE IF NOT EXISTS accounts (
                	"account_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                	"type"	INTEGER,
                	"remains"	REAL,
                	"status"	INTEGER,
                	"user_id"	INTEGER,
                	FOREIGN KEY("user_id") REFERENCES "users"("user_id")
                );"""
        print(query)
        cursor.execute(query)
        db.commit()   

def create_operations(db_name: str):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS "operations" (
                        "operation_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        "amount"	INTEGER,
                        "account_id"	INTEGER,
                        "time"	INTEGER,
                        "type"	INTEGER,
                        FOREIGN KEY("account_id") REFERENCES "accounts"("account_id")
                    );"""
            print(query)
            cursor.execute(query)
            db.commit() 

db_name = 'sovkombank_db'

create_accounts(db_name)
create_operations(db_name)
print('end')





