from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def mostrarespecie():
    cursor = con.cursor()
    cursor.execute ("SELECT id_especie, nombre_especie FROM especie")
    especie = cursor.fetchall()
    cursor.close()
    return especie

def mostrarraza(idespecie):
    cursor = con.cursor()
    cursor.execute ("SELECT idraza, nombre_raza FROM municipio WHERE id_especie = ?", idespecie)
    raza = cursor.fetchall()
    cursor.close()
    return raza