import pyodbc

class ConnectionManager:
    _user = None
    _password = None
    _connection = None
    _last_error = None

    @classmethod
    def set_credentials(cls, user, password):
        cls._user = user
        cls._password = password
        cls._connection = None  # Forzar reconexión

    @classmethod
    def get_connection(cls):
        if cls._connection:
            return cls._connection
        if not cls._user or not cls._password:
            print("No hay credenciales definidas")
            return None
        try:
            cnxn_str = (
                "Driver={SQL Server};"
                "Server=servidorbelen.database.windows.net"
                "Database=genesis;"
                f"UID={cls._user};"
                f"PWD={cls._password};"
                "Trusted_Connection=no;"
            )
            cls._connection = pyodbc.connect(cnxn_str)
            return cls._connection
        except pyodbc.Error as e:
            print("Error al conectar con la base de datos:", e)
            return None
        
    @classmethod
    def get_last_error(cls):  # <- NUEVO
        return cls._last_error

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None


# cnxn_str = (
#     "Driver={SQL Server};"
#     "Server=DESKTOP-EEVISNL\\SQLEXPRESS;"
#     "Database=genesis;"
#     "UID=;"
#     "PWD=belen2025!*;"
# )
