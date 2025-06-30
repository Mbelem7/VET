from modulos.coneccion import *
import pyodbc


def mostrarcategoriasp():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT id_tipocliente, tipocliente FROM tipo_cliente")
    categoriap = cursor.fetchall()
    cursor.close()
    return categoriap