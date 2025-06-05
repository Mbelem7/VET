from modulos.coneccion import BDconeccion
import pyodbc

def obtener_reporte_propietarios():
    con = BDconeccion()
    cursor = con.cursor()
    query = """
       SELECT 
    p.ID_PROPIETARIO,
    per.NOMBRE,
    per.APELLIDO,
    per.CEDULA,
    per.TELEFONO,
    per.CORREO,
    per.DIRECCION,
    tc.TIPOCLIENTE AS TIPO_CLIENTE,
    p.ESTADO,
    m.NOMBRE_MASCOTA AS MASCOTA
FROM PROPIETARIO p
JOIN PERSONA per ON p.PERSONA_ID = per.ID_PERSONA
JOIN TIPO_CLIENTE tc ON p.TIPOCLIENTE_ID = tc.ID_TIPOCLIENTE
LEFT JOIN MASCOTA m ON p.MASCOTA_ID = m.ID_MASCOTA
ORDER BY per.APELLIDO, per.NOMBRE;
    """
    cursor.execute(query)
    columnas = [col[0] for col in cursor.description]
    datos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    con.close()
    return datos