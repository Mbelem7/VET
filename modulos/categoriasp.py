from modulos.coneccion import *
import pyodbc

con = ConnectionManager.get_connection()

def mostrarcategoriasp():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT id_tipocliente, tipocliente FROM tipo_cliente")
    categoriap = cursor.fetchall()
    cursor.close()
    return categoriap