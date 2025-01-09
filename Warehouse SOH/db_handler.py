import psycopg2
import os

def connect_db():
    """Establishes a connection to the database."""
    try:
        conn = psycopg2.connect(
            host="192.168.1.13",
            port=5432,
            dbname="postgres",
            user="postgres",
            password="mbpi"
        )
        return conn
    except psycopg2.Error as e:
        raise ConnectionError(f"Error connecting to the database: {e}")

def authenticate_user(username, password):
    """Checks if the username and password match a record in the database."""
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT * FROM warehouse_program.warehouse_user WHERE user_name = %s AND password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # Log the user login
            log_query = """
            INSERT INTO warehouse_program.logs (user_name, computer_name, timestamp)
            VALUES (%s, %s, NOW())
            """
            cursor.execute(log_query, (username, os.environ['COMPUTERNAME']))
            conn.commit()
            return user  # Return user details for further use
        else:
            return None
    except psycopg2.Error as e:
        raise RuntimeError(f"Database error: {e}")
    finally:
        if conn:
            conn.close()