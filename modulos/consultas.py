from modulos.coneccion import *
import pyodbc


def insertarconsulta(fecha_consulta, descripcion_consulta, diagnostico, tratamiento, precio_consulta, mascota_id):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO CONSULTA (FECHA_CONSULTA, DESCRIPCION_CONSULTA, DIAGNOSTICO, TRATAMIENTO, PRECIO_CONSULTA, MASCOTA_ID)
        OUTPUT INSERTED.ID_CONSULTA
        VALUES (?, ?, ?, ?, ?, ?)
    """, (fecha_consulta, descripcion_consulta, diagnostico, tratamiento, precio_consulta, mascota_id))
    consulta_id = cursor.fetchone()[0]
    con.commit()
    cursor.close()
    return consulta_id

def insertar_consulta_medicamento(id_consulta, id_producto, dosis, duracion):
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO CONSULTA_MEDICAMENTO (ID_CONSULTA, ID_PRODUCTO, DOSIS, DURACION)
        VALUES (?, ?, ?, ?)
    """, (id_consulta, id_producto, dosis, duracion))
    con.commit()
    cursor.close()

def mostrar_consultas():
    con = ConnectionManager.get_connection()
    cursor = con.cursor()
    cursor.execute("""
        SELECT 
            c.ID_CONSULTA,
            m.NOMBRE_MASCOTA,
            m.PESO,
            m.EDAD,
            c.FECHA_CONSULTA,
            c.DESCRIPCION_CONSULTA,
            c.PRECIO_CONSULTA,
            ISNULL(SUM(p.PRECIO_PRODUCTO), 0) as total_medicamentos
        FROM CONSULTA c
        JOIN MASCOTA m ON c.MASCOTA_ID = m.ID_MASCOTA
        LEFT JOIN CONSULTA_MEDICAMENTO cm ON c.ID_CONSULTA = cm.ID_CONSULTA
        LEFT JOIN PRODUCTO p ON cm.ID_PRODUCTO = p.ID_PRODUCTO
        GROUP BY c.ID_CONSULTA, m.NOMBRE_MASCOTA, m.PESO, m.EDAD, c.FECHA_CONSULTA, c.DESCRIPCION_CONSULTA, c.PRECIO_CONSULTA
        ORDER BY c.FECHA_CONSULTA DESC
    """)
    consultas = []
    for row in cursor.fetchall():
        total = (row[6] or 0) + (row[7] or 0)
        consultas.append({
            'id': row[0],
            'mascota': row[1],
            'peso': row[2],
            'edad': row[3],
            'fecha': row[4],
            'descripcion': row[5],
            'total': total
        })
    cursor.close()
    return consultas