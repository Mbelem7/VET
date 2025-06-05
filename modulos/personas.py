from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarpersona(nombre, apellido, cedula, telefono, correo, direccion):
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO persona (nombre, apellido, cedula, telefono, correo, direccion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellido, cedula, telefono, correo, direccion))
        cursor.execute("SELECT SCOPE_IDENTITY()")
        persona_id = cursor.fetchone()[0]
        con.commit()
        cursor.close()
        return persona_id
    except Exception as e:
        print("Error en insertarpersona:", e)
        return None

    