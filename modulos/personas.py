from modulos.coneccion import *
import pyodbc

con = ConnectionManager.get_connection()

def insertarpersona(nombre, apellido, cedula, telefono, correo, direccion):
    try:
        con = ConnectionManager.get_connection()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO persona (nombre, apellido, cedula, telefono, correo, direccion)
            OUTPUT INSERTED.ID_PERSONA
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, cedula, telefono, correo, direccion))
        
        persona_id = cursor.fetchone()[0]
        con.commit()
        cursor.close()
        return persona_id
    except Exception as e:
        print("Error en insertarpersona:", e)
        import traceback
        traceback.print_exc()
        return None

def obtener_id_persona(username):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT PERSONA_IDU FROM USUARIOS WHERE USUARIO = ?", (username,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None
    