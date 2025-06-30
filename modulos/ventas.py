from modulos.coneccion import *
import pyodbc

def obtener_tipo_venta(producto_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT TIPO_VENTA FROM PRODUCTO WHERE ID_PRODUCTO = ?", (producto_id,))
    tipo = cursor.fetchone()
    cursor.close()
    return tipo[0] if tipo else 'unidad'

def obtener_stock_unidades(producto_id):
    con = ConnectionManager.get_connection()
    if not con:
        raise Exception("No hay conexión a la base de datos. Verifique sus credenciales o sesión.")
    cursor = con.cursor()
    cursor.execute("SELECT STOCK_UNIDADES FROM PRODUCTO WHERE ID_PRODUCTO = ?", (producto_id,))
    stock = cursor.fetchone()
    cursor.close()
    return stock[0] if stock else 0

def obtener_stock_peso(producto_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("SELECT STOCK_PESO FROM PRODUCTO WHERE ID_PRODUCTO = ?", (producto_id,))
    stock = cursor.fetchone()
    cursor.close()
    return stock[0] if stock else 0

def descontar_stock(producto_id, cantidad):
    tipo_venta = obtener_tipo_venta(producto_id)
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    if tipo_venta == 'unidad':
        cursor.execute(
            "UPDATE PRODUCTO SET STOCK_UNIDADES = STOCK_UNIDADES - ? WHERE ID_PRODUCTO = ?",
            (int(cantidad), producto_id)
        )
    elif tipo_venta == 'peso':
        cursor.execute(
            "UPDATE PRODUCTO SET STOCK_PESO = STOCK_PESO - ? WHERE ID_PRODUCTO = ?",
            (float(cantidad), producto_id)
        )
    con.commit()
    cursor.close()

def insertar_venta(fecha, total, persona_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO VENTA (FECHA_VENTA, TOTAL_VENTA, PERSONA_ID_VENTA)
        OUTPUT INSERTED.ID_VENTA
        VALUES (?, ?, ?)
    """, (fecha, total, persona_id))
    
    venta_id = cursor.fetchone()[0]
    con.commit()
    cursor.close()
    print(venta_id)
    return venta_id

def insertar_detalle_venta(venta_id, producto_id, cantidad, subtotal):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO DETALLE_VENTA (VENTA_ID, PRODUCTO_ID, CANTIDAD, SUBTOTAL)
                   
        VALUES (?, ?, ?, ?)
    """, (venta_id, producto_id, cantidad, subtotal))
    con.commit()
    cursor.close()

def validar_cantidad(producto_id, cantidad):
    tipo_venta = obtener_tipo_venta(producto_id)
    if tipo_venta == 'unidad':
        if not float(cantidad).is_integer():
            raise ValueError("Solo se permiten cantidades enteras para este producto.")
        stock = obtener_stock_unidades(producto_id)
        if int(cantidad) > stock:
            raise ValueError("No hay suficientes unidades.")
        return int(cantidad), tipo_venta
    else:
        stock = obtener_stock_peso(producto_id)
        if float(cantidad) > stock:
            raise ValueError("No hay suficiente peso disponible.")
        return float(cantidad), tipo_venta

def mostrar_ventas(id_venta=None):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    base_query = '''
        SELECT
            v.ID_VENTA,
            v.FECHA_VENTA,
            p.nombre AS nombre_persona,
            p.apellido AS apellido_persona,
            pr.NOMBRE_PRODUCTO,
            dv.CANTIDAD,
            pr.TIPO_VENTA,
            v.TOTAL_VENTA, -- total de la venta
            pr.PRECIO_PRODUCTO,
            pr.PRECIO_UNITARIO
        FROM
            VENTA v
        INNER JOIN persona p ON v.PERSONA_ID_VENTA = p.id_persona
        INNER JOIN DETALLE_VENTA dv ON v.ID_VENTA = dv.VENTA_ID
        INNER JOIN PRODUCTO pr ON dv.PRODUCTO_ID = pr.ID_PRODUCTO
    '''
    if id_venta is None:
        cursor.execute(base_query)
    else:
        query_with_where = base_query + " WHERE v.ID_VENTA = ?"
        cursor.execute(query_with_where, (id_venta,))
    rows = cursor.fetchall()
    cursor.close()
    ventas = []
    for row in rows:
        # row: (ID_VENTA, FECHA_VENTA, nombre, apellido, NOMBRE_PRODUCTO, CANTIDAD, TIPO_VENTA, TOTAL_VENTA, PRECIO_PRODUCTO, PRECIO_UNITARIO)
        if row[6] == 'unidad':
            precio = row[8]
        else:
            precio = row[9]
        ventas.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], precio, row[7]))
    return ventas

