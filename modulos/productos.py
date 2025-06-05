from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarproducto (nombreproducto, descripcion, precio, unidades, categoria):
    cursor = con.cursor()
    cursor.execute ("""INSERT INTO mascota
                        (nombre_producto, descripcion_producto, precio_producto, stock, categoria_id) 
                    VALUES (?, ?, ?, ?, ?)""", nombreproducto, descripcion, precio, unidades, categoria)
    cursor.commit()
    cursor.close()

