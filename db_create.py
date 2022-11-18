import sqlite3

def create_roles(db_name : str):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        query = """
                    CREATE TABLE IF NOT EXISTS roles(
                    id	INTEGER,
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
                    ID	INTEGER,
                    login	TEXT ,
                    password	TEXT,
                    status	INTEGER,
                    role_id	INTEGER,
                    FOREIGN KEY(role_id) REFERENCES roles(id)
                    );"""
        print(query)
        cursor.execute(query)
        db.commit()

db_name = 'sovkombank_db'
create_roles(db_name)
create_users(db_name)

print('end')





