from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def mostrarcategoria():
    cursor = con.cursor()
    cursor.execute ("SELECT ID_CATEGORIA, NOMBRE_CATEGORIA FROM CATEGORIA_PRODUCTO")
    categ = cursor.fetchall()
    cursor.close()
    return categ