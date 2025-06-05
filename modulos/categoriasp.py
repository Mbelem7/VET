from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def mostrarcategoriasp():
    cursor = con.cursor()
    cursor.execute ("SELECT id_tipocliente, tipocliente FROM tipo_cliente")
    categoriap = cursor.fetchall()
    cursor.close()
    return categoriap