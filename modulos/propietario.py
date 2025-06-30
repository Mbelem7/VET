from modulos.coneccion import *
import pyodbc

def insertarpropietario(persona_id, tipocliente_id, estado):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO propietario (persona_id, tipocliente_id, estado)
        VALUES (?, ?, ?)
    """, (persona_id, tipocliente_id, estado))
    con.commit()
    cursor.close()

def mostrarpropietarios():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT prop.id_propietario, per.id_persona, per.nombre, prop.estado, prop.tipocliente_id
        FROM propietario AS prop
        INNER JOIN persona AS per ON per.id_persona = prop.persona_id
    """)
    propietarios = cursor.fetchall()
    cursor.close()
    return propietarios

def buscarpropietario_por_correo(correo):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT per.nombre, per.apellido, per.cedula, per.telefono, per.correo, per.direccion
        FROM persona AS per
        INNER JOIN propietario AS prop ON per.id_persona = prop.persona_id
        WHERE per.correo = ?
    """, (correo,))
    prop = cursor.fetchone()
    cursor.close()
    return prop
