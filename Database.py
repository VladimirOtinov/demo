import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="silkweb"
            )
            return True
        except Error as e:
            print(f"Ошибка подключения к MySQL: {e}")
            return False

    def check_credentials(self, login, password):
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            query = """SELECT u.email, r.name as role 
                       FROM users u 
                       JOIN roles r ON u.role_id = r.id 
                       WHERE u.email = %s AND u.password = %s"""
            cursor.execute(query, (login, password))
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Ошибка проверки учетных данных: {e}")
            return None
        finally:
            cursor.close()