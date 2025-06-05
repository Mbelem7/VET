from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarmascota (nombremascota, edad, peso, sexo, raza):
    cursor = con.cursor()
    cursor.execute ("""INSERT INTO mascota
                        (nombre_mascota, edad, peso, sexo, raza_id) 
                    VALUES (?, ?, ?, ?, ?)""", nombremascota, edad, peso, sexo, raza)
    cursor.commit()
    cursor.close()

def mostrarmacota(idmascota):
    cursor = con.cursor()
    cursor.execute ("""SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
        per.nombre AS nombre_propietario, per.correo
        FROM mascota AS mas
        INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
        INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
        INNER JOIN persona AS per ON prop.persona_id = per.id_persona
        WHERE mas.id_mascota = ? """, idmascota)
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas

def mostrartodaslasmascotas():
    cursor = con.cursor()
    cursor.execute("SELECT id_mascota, nombre_mascota FROM mascota")
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas


def buscarmascota(telf):
    cursor = con.cursor()
    cursor.execute ("""SELECT mas.id_mascota
        FROM mascota AS mas
        INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
        INNER JOIN persona AS per ON prop.persona_id = per.id_persona
        WHERE per.telefono = ?""", telf)
    id_mascota = cursor.fetchone()
    return id_mascota[0]

def buscarmascotaportelf(telf):
    id_mascota = buscarmascota(telf)
    cursor = con.cursor()
    cursor.execute ("SELECT id_mascota FROM mascota WHERE id_mascota = ?", id_mascota)
    id_mascota = cursor.fetchone()
    return id_mascota[0]

