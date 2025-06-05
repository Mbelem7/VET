from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarpersona(nombre, apellido, cedula, telefono, correo, direccion):
    try:
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


    