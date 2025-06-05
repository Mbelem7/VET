from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarpropietario(persona_id, tipocliente_id, mascota_id):
    cursor = con.cursor()
    cursor.execute("""INSERT INTO propietario 
                      (persona_id, tipocliente_id, mascota_id)
                      VALUES (?, ?, ?)""", 
                   (persona_id, tipocliente_id, mascota_id))
    con.commit()
    cursor.close()