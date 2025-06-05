from modulos.coneccion import BDconeccion
import pyodbc
from werkzeug.security import check_password_hash

con = BDconeccion()

#para buscar usuario
def buscarUsuario(Usuario,contraseña):
    cursor = con.cursor()
    cursor.execute("SELECT CONTRASEÑA FROM USUARIOS WHERE USUARIO = ?",Usuario)
    ContraseñaEncriptada = cursor.fetchone()
    cursor.close()
    if ContraseñaEncriptada is None:
        return False
    if check_password_hash(ContraseñaEncriptada[0],contraseña):
        return True
    else:
        return False

#verificar que el usuario tenga un rol
def rolesPorUsuario(usuario):
    cursor = con.cursor()
    cursor.execute("""  SELECT R.ROLES
                        FROM	ROLES AS R
                        INNER JOIN USUARIOS AS U ON U.ID_USUARIOS = R.USUARIO_IDR
                        WHERE U.USUARIO LIKE ? """, usuario)
    roles = cursor.fetchall()
    cursor.close()
    return roles if roles else None