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

def mostrarmacota(idmascota=None):
    cursor = con.cursor()
    if idmascota is None:
        cursor.execute("""
            SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
                   per.nombre, per.cedula, per.telefono, per.correo, per.direccion, prop.estado, mas.id_mascota
            FROM mascota AS mas
            INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
            INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
            INNER JOIN persona AS per ON prop.persona_id = per.id_persona
        """)
    else:
        cursor.execute("""
            SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
                   per.nombre, per.cedula, per.telefono, per.correo, per.direccion, prop.estado, mas.id_mascota
            FROM mascota AS mas
            INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
            INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
            INNER JOIN persona AS per ON prop.persona_id = per.id_persona
            WHERE mas.id_mascota = ?
        """, (idmascota,))
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas

# def mostrarmacota(idmascota=None):
#     cursor = con.cursor()
#     if idmascota is None:
#         cursor.execute("""
#             SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
#                    per.id_persona, mas.id_mascota
#             FROM mascota AS mas
#             INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
#             INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
#             INNER JOIN persona AS per ON prop.persona_id = per.id_persona
#         """)
#     else:
#         cursor.execute("""
#             SELECT mas.nombre_mascota, mas.edad, mas.peso, mas.sexo, raz.nombre_raza,
#                    per.id_persona, mas.id_mascota
#             FROM mascota AS mas
#             INNER JOIN raza AS raz ON mas.raza_id = raz.id_raza
#             INNER JOIN propietario AS prop ON mas.id_mascota = prop.mascota_id
#             INNER JOIN persona AS per ON prop.persona_id = per.id_persona
#             WHERE mas.id_mascota = ?
#         """, (idmascota,))
#     mascotas = cursor.fetchall()
#     cursor.close()
#     return mascotas

def mostrartodaslasmascotas():
    cursor = con.cursor()
    cursor.execute("SELECT id_mascota, nombre_mascota FROM mascota")
    mascotas = cursor.fetchall()
    cursor.close()
    return mascotas

def actualizar_mascota(idmascota, edad, peso, propietario_id):
    cursor = con.cursor()
    cursor.execute("""
        UPDATE mascota
        SET edad = ?, peso = ?
        WHERE id_mascota = ?
    """, (edad, peso, idmascota))
    cursor.execute("""
        UPDATE propietario
        SET persona_id = ?
        WHERE mascota_id = ?
    """, (propietario_id, idmascota))
    con.commit()
    cursor.close()
