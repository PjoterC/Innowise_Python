import psycopg2 as pg

class DbConnector:
    def __init__(self):
        pass
    
    def CreateConnection(db_name, db_user, db_password, db_host="localhost", db_port="5432"):
        """
        Create a connection to the PostgreSQL database.
        """
        try:
            conn = pg.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            print("✅ Connection successful")
            return conn
        except pg.OperationalError as e:
            print(f"Error: {e}")
            return None

DbConnector.CreateConnection(db_name="innowise_python_postgres", db_user="user", db_password="password")