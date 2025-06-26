from modulos.coneccion import *
import pyodbc

con = ConnectionManager.get_connection()

def insertarmascota (nombremascota, edad, peso, sexo, raza, propietario_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("""INSERT INTO mascota
                        (nombre_mascota, edad, peso, sexo, raza_id, propietario_id)
                    VALUES (?, ?, ?, ?, ?, ?)""", (nombremascota, edad, peso, sexo, raza, propietario_id))
    cursor.commit()
    cursor.close()

def mostrarmacota(idmascota=None):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    if idmascota is None:
        cursor.execute("""  
            SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
                   (per.nombre + ' ' + per.apellido) AS nombre_completo, per.cedula, per.telefono, per.correo, per.direccion, prop.estado, mas.id_mascota
            FROM mascota AS mas
            INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
            INNER JOIN propietario AS prop ON mas.propietario_id = prop.id_propietario
            INNER JOIN persona AS per ON prop.persona_id = per.id_persona
        """)
    else:
        cursor.execute("""
            SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
                   (per.nombre + ' ' + per.apellido) AS nombre_completo, per.cedula, per.telefono, per.correo, per.direccion, prop.estado, mas.id_mascota
            FROM mascota AS mas
            INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
            INNER JOIN propietario AS prop ON mas.propietario_id = prop.id_propietario
            INNER JOIN persona AS per ON prop.persona_id = per.id_persona
            WHERE mas.id_mascota = ?
        """, (idmascota,))
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas


def mostrartodaslasmascotas():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT id_mascota, nombre_mascota FROM mascota")
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas

def actualizar_mascota(idmascota, edad, peso, propietario_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE mascota
        SET edad = ?, peso = ?, propietario_id = ?
        WHERE id_mascota = ?
    """, (edad, peso, propietario_id, idmascota))
    con.commit()
    cursor.close()
