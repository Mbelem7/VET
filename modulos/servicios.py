from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertar_servicio(nombre_servicio, imagen_url, precio, descripcion):
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO SERVICIO
            (NOMBRE_SERVICIO, IMAGEN_URL, PRECIO, DESCRIPCION)
        VALUES (?, ?, ?, ?)
    """, nombre_servicio, imagen_url, precio, descripcion)
    con.commit()
    cursor.close()

def obtener_servicios():
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_SERVICIO, NOMBRE_SERVICIO, IMAGEN_URL, PRECIO, DESCRIPCION
        FROM SERVICIO
    """)
    servicios = cursor.fetchall()
    cursor.close()
    return servicios