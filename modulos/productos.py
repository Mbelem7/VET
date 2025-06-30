from modulos.coneccion import *
import pyodbc

def insertarproducto(nombreproducto, imagenurl, descripcion, precio, precio_unitario, unidades, peso_por_unidad, stock_peso, tipo_venta, categoria):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO PRODUCTO
            (NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, PRECIO_UNITARIO, STOCK_UNIDADES, PESO_POR_UNIDAD, STOCK_PESO, TIPO_VENTA, CATEGORIA_ID)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, nombreproducto, imagenurl, descripcion, precio, precio_unitario, unidades, peso_por_unidad, stock_peso, tipo_venta, categoria)
    con.commit()
    cursor.close()

def obtener_productos():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, PRECIO_UNITARIO, STOCK_UNIDADES, PESO_POR_UNIDAD, STOCK_PESO, TIPO_VENTA
        FROM PRODUCTO
    """)
    productos = cursor.fetchall()
    cursor.close()
    return productos

def obtenerunproducto(idproducto):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, IMAGENURL, DESCRIPCION_PRODUCTO, PRECIO_PRODUCTO, PRECIO_UNITARIO, STOCK_UNIDADES, PESO_POR_UNIDAD, STOCK_PESO, TIPO_VENTA
        FROM PRODUCTO
        WHERE ID_PRODUCTO = ?
    """, (idproducto,))
    producto = cursor.fetchone()
    cursor.close()
    return producto

def actualizar_producto(id_producto, precio, precio_unitario, stock_unidades, peso_por_unidad, stock_peso, tipo_venta, estado):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE PRODUCTO
        SET PRECIO_PRODUCTO = ?, PRECIO_UNITARIO = ?, STOCK_UNIDADES = ?, PESO_POR_UNIDAD = ?, STOCK_PESO = ?, TIPO_VENTA = ?, ESTADO = ?
        WHERE ID_PRODUCTO = ?
    """, (precio, precio_unitario, stock_unidades, peso_por_unidad, stock_peso, tipo_venta, estado, id_producto))
    con.commit()
    cursor.close()

# para la consulta medica
def obtener_medicamentos():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, PRECIO_PRODUCTO 
        FROM PRODUCTO
        WHERE CATEGORIA_ID = 4  -- ID de Medicamento
    """)
    medicamentos = cursor.fetchall()
    cursor.close()
    return medicamentos