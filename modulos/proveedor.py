from modulos.coneccion import *
import pyodbc

def insertarproveedor(persona_id, nombre_empresa, categoria_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO PROVEEDOR (PERSONA_ID, NOMBRE_EMPRESA, CATEGORIA_ID)
        VALUES (?, ?, ?)
    """, (persona_id, nombre_empresa, categoria_id))
    con.commit()
    cursor.close()

def mostrarproveedores():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT prov.ID_PROVEEDOR, per.ID_PERSONA, per.NOMBRE, per.APELLIDO, per.CEDULA, per.TELEFONO, per.CORREO, per.DIRECCION,
               prov.NOMBRE_EMPRESA, prov.CATEGORIA_ID
        FROM PROVEEDOR AS prov
        INNER JOIN PERSONA AS per ON per.ID_PERSONA = prov.PERSONA_ID
    """)
    proveedores = cursor.fetchall()
    cursor.close()
    return proveedores