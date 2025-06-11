from modulos.coneccion import BDconeccion
import pyodbc

con = BDconeccion()

def insertarproducto(nombreproducto, imagenurl, descripcion, precio, unidades, categoria):
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO PRODUCTO
            (NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, STOCK, CATEGORIA_ID)
        VALUES (?, ?, ?, ?, ?, ?)
    """, nombreproducto, imagenurl, descripcion, precio, unidades, categoria)
    con.commit()
    cursor.close()

def obtener_productos():
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, STOCK
        FROM PRODUCTO
    """)
    productos = cursor.fetchall()
    cursor.close()
    return productos

def obtenerunproducto(idproducto):
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, STOCK
        FROM PRODUCTO
        WHERE ID_PRODUCTO = ?
    """, (idproducto,))
    producto = cursor.fetchone()
    cursor.close()
    return producto

def actualizar_producto(id_producto, precio, stock):
    cursor = con.cursor()
    cursor.execute("""
        UPDATE PRODUCTO
        SET PRECIO_PRODUCTO = ?, STOCK = ?
        WHERE ID_PRODUCTO = ?
    """, (precio, stock, id_producto))
    con.commit()
    cursor.close()
