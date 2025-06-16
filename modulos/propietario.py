from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarpropietario(persona_id, tipocliente_id, mascota_id, estado):
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO propietario (persona_id, tipocliente_id, mascota_id, estado)
        VALUES (?, ?, ?, ?)
    """, (persona_id, tipocliente_id, mascota_id, estado))
    con.commit()
    cursor.close()

def mostrarpropietarios():
    cursor = con.cursor()
    cursor.execute("""
        SELECT per.id_persona, per.nombre
        FROM persona AS per
        INNER JOIN propietario AS prop ON per.id_persona = prop.persona_id
    """)
    propietarios = cursor.fetchall()
    cursor.close()
    return propietarios