import mysql.connector

def get_mysql_connection(host="localhost", user="root", password="", database=None):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("✅ Connected to MySQL")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection error: {err}")
        return None

