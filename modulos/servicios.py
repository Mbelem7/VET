from modulos.coneccion import *
import pyodbc

def insertarserviciocatalogo(nombre_servicio, imagen_url, precio, descripcion):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO CATALOGO_SERVICIOS
            (NOMBRE_SERVICIO, IMAGENURL, PRECIO_ESTIMADO, DESCRIPCION)
        VALUES (?, ?, ?, ?)
    """, nombre_servicio, imagen_url, precio, descripcion)
    con.commit()
    cursor.close()

def obtener_servicio(idcatalogo):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_CATALOGO, NOMBRE_SERVICIO, IMAGENURL, PRECIO_ESTIMADO, DESCRIPCION, ESTADO
        FROM CATALOGO_SERVICIOS
        WHERE ID_CATALOGO = ?
    """, (idcatalogo,))
    servicio = cursor.fetchone()
    cursor.close()
    return servicio

# Devuelve todos los servicios
def obtener_servicios():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT ID_CATALOGO, NOMBRE_SERVICIO, IMAGENURL, PRECIO_ESTIMADO, DESCRIPCION, ESTADO
        FROM CATALOGO_SERVICIOS
    """)
    servicios = cursor.fetchall()
    cursor.close()
    return servicios

def mostrarservicio():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute ("SELECT ID_CATALOGO, NOMBRE_SERVICIO,  PRECIO_ESTIMADO, DESCRIPCION  FROM CATALOGO_SERVICIOS")
    ser = cursor.fetchall()
    cursor.close()
    return ser

def insertar_servicio(fecha, total, mascota_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO SERVICIOS (FECHA_SERVICIO, TOTAL_SERVICIO, MASCOTA_ID)
        OUTPUT INSERTED.ID_SERVICIOS
        VALUES (?, ?, ?)
    """, (fecha, total, mascota_id))
    servicio_id = cursor.fetchone()[0]
    con.commit()
    cursor.close()
    print(servicio_id)
    return servicio_id

def insertar_detalle_servicio(servicio_id, catalogo_servicio_id, precio):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    # Opción 1: Si siempre es cantidad 1
    cursor.execute("""
        INSERT INTO DETALLE_SERVICIO (ID_SERVICIOS, ID_CATALOGO, CANTIDAD, PRECIO_UNITARIO)
        VALUES (?, ?, ?, ?)
    """, (servicio_id, catalogo_servicio_id, 1, precio)) # Se agrega '1' para CANTIDAD
    con.commit()


def mostrar_servicios(id_servicio_principal=None):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    base_query = """
        SELECT
            mas.NOMBRE_MASCOTA,
            ser.FECHA_SERVICIO,
            cat.NOMBRE_SERVICIO,
            cat.DESCRIPCION,
            det.PRECIO_UNITARIO -- Ahora seleccionamos directamente el PRECIO_UNITARIO del detalle
        FROM
            dbo.SERVICIOS AS ser
        INNER JOIN
            dbo.MASCOTA AS mas ON ser.MASCOTA_ID = mas.ID_MASCOTA
        INNER JOIN
            dbo.DETALLE_SERVICIO AS det ON ser.ID_SERVICIOS = det.ID_SERVICIOS
        INNER JOIN
            dbo.CATALOGO_SERVICIOS AS cat ON det.ID_CATALOGO = cat.ID_CATALOGO
    """

    if id_servicio_principal is None:
        cursor.execute(base_query)
    else:
        query_with_where = base_query + """
            WHERE ser.ID_SERVICIOS = ?
        """
        cursor.execute(query_with_where, (id_servicio_principal,))

    servicios = cursor.fetchall()
    cursor.close()
    return servicios

#ACTUALIZAR SERVICIO
def actualizar_servicio(idcatalogo, precio, estado):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE CATALOGO_SERVICIOS
        SET PRECIO_ESTIMADO = ?, ESTADO = ?
        WHERE ID_CATALOGO = ?
    """, (precio, estado, idcatalogo))
    con.commit()
    cursor.close()
