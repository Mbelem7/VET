import pyodbc
def BDconeccion():
    cnxn_str = ("Driver={SQL Server};"
                    "Server=DESKTOP-BK6VRQ8\SQL19;"
                    "Database=genesis;"
                    "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    return cnxn
