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
    cursor.execute ("SELECT id_raza, nombre_raza FROM RAZA WHERE ESPECIE_ID = ?", idespecie)
    raza = cursor.fetchall()
    cursor.close()
    return raza

def mostrarraza_todas():
    cursor = con.cursor()
    cursor.execute("SELECT id_raza, nombre_raza FROM raza")
    razas = cursor.fetchall()
    cursor.close()
    return razas