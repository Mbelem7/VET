import pyodbc
def BDconeccion():
    cnxn_str = ("Driver={SQL Server};"
                    "Server=DESKTOP-EEVISNL\\SQLEXPRESS;"
                    "Database=VETPRUEBA;"
                    "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    return cnxn
