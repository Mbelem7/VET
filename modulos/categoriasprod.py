from modulos.coneccion import *
import pyodbc

con = ConnectionManager.get_connection()

def mostrarcategoria():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT ID_CATEGORIA, NOMBRE_CATEGORIA FROM CATEGORIA_PRODUCTO")
    categ = cursor.fetchall()
    cursor.close()
    return categ