from modulos.coneccion import *
import pyodbc

def mostrarespecie():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT id_especie, nombre_especie FROM especie")
    especie = cursor.fetchall()
    cursor.close()
    return especie

def mostrarraza(idespecie):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT id_raza, nombre_raza FROM RAZA WHERE ESPECIE_ID = ?", idespecie)
    raza = cursor.fetchall()
    cursor.close()
    return raza

def mostrarraza_todas():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT id_raza, nombre_raza FROM raza")
    razas = cursor.fetchall()
    cursor.close()
    return razas