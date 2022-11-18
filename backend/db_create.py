import sqlite3

def create_roles(db_name : str):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        query = """
                    CREATE TABLE IF NOT EXISTS roles(
                    role_id	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name_role	TEXT
                    );"""
        print(query)
        cursor.execute(query)
        db.commit()

def create_users(db_name : str):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        query = """
                    CREATE TABLE IF NOT EXISTS users(
                    user_id	INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    login	TEXT ,
                    password	TEXT,
                    role_id	INTEGER,
                    FOREIGN KEY(role_id) REFERENCES roles(role_id)
                    );"""
        print(query)
        cursor.execute(query)
        db.commit()

db_name = 'sovkombank_db'
create_roles(db_name)
create_users(db_name)

print('end')





