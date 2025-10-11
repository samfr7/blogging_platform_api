from mysql.connector import connection, Error
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = connection.MySQLConnection(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )

    cursor = conn.cursor()

    cursor.execute('CREATE DATABASE IF NOT EXISTS blogging_platform')
    result = cursor.fetchall()
    print(result)
except Error as e:
    print(e)
finally:
    cursor.close()
    conn.close()



