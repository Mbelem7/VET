from modulos.coneccion import ConnectionManager
from werkzeug.security import check_password_hash

def buscarUsuario(Usuario, contraseña):
    con = ConnectionManager.get_connection()
    if not con:
        return False
    cursor = con.cursor()
    cursor.execute("SELECT CONTRASEÑA FROM USUARIOS WHERE USUARIO = ?", Usuario)
    ContraseñaEncriptada = cursor.fetchone()
    cursor.close()
    if ContraseñaEncriptada is None:
        return False
    return check_password_hash(ContraseñaEncriptada[0], contraseña)

def rolesPorUsuario(usuario):
    con = ConnectionManager.get_connection()
    if not con:
        return None
    cursor = con.cursor()
    cursor.execute("""
        SELECT r.name AS Rol
        FROM sys.database_role_members drm
        JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
        JOIN sys.database_principals u ON drm.member_principal_id = u.principal_id
        WHERE u.name = ?;
    """, usuario)
    roles = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    return roles if roles else None
