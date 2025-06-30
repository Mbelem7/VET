import os
import pyodbc

class ConnectionManager:
    _connection = None
    _last_error = None

    @classmethod
    def get_connection(cls):
        if cls._connection:
            return cls._connection
        # Leer credenciales desde variables de entorno
        server = os.environ.get('AZURE_SQL_SERVER')
        database = os.environ.get('AZURE_SQL_DATABASE')
        user = os.environ.get('AZURE_SQL_USER')
        password = os.environ.get('AZURE_SQL_PASSWORD')
        if not all([server, database, user, password]):
            print("Faltan variables de entorno para la conexión a Azure SQL Database")
            cls._last_error = "Faltan variables de entorno"
            return None
        try:
            cnxn_str = (
                "Driver={ODBC Driver 17 for SQL Server};"
                f"Server={server};"
                f"Database={database};"
                f"UID={user};"
                f"PWD={password};"
                "Encrypt=yes;"
                "TrustServerCertificate=no;"
            )
            cls._connection = pyodbc.connect(cnxn_str)
            return cls._connection
        except pyodbc.Error as e:
            print("Error al conectar con la base de datos:", e)
            cls._last_error = str(e)
            return None

    @classmethod
    def get_last_error(cls):
        return cls._last_error

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
