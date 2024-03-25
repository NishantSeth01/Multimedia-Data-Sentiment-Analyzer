import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="user",
            auth_plugin='mysql_native_password'
        )
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
        """)
        self.connection.commit()

    def insert_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        self.connection.commit()

    def validate_login(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE BINARY username=%s AND BINARY password=%s", (username, password))
        user = cursor.fetchone()
        return user

    def validate_signup(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()
        return existing_user