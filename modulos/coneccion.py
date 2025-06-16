import pyodbc
def BDconeccion():
    cnxn_str = ("Driver={SQL Server};"
                    "Server=DESKTOP-EEVISNL\\SQLEXPRESS;"
                    "Database=genesis;"
                    "Trusted_Connection=yes;")
    cnxn = pyodbc.connect(cnxn_str)
    return cnxn


# cnxn_str = (
#     "Driver={SQL Server};"
#     "Server=DESKTOP-EEVISNL\\SQLEXPRESS;"
#     "Database=genesis;"
#     "UID=;"
#     "PWD=belen2025!*;"
# )
