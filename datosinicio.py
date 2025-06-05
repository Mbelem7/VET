from modulos.coneccion import *
from werkzeug.security import generate_password_hash

def insertarPersona():
    try:
        con = BDconeccion()
        cursor = con.cursor()
        cursor.execute(""" IF NOT EXISTS (SELECT 1 FROM PERSONA WHERE CEDULA = '000-000000-0000A')
                           BEGIN
                                INSERT INTO PERSONA (NOMBRE,APELLIDO,CEDULA,TELEFONO,CORREO,DIRECCION)
                                VALUES (?,?,?,?,?,?)
                            END""",'Administrador', 'Sistema', '000-000000-0000A', 
                                '80900000', 'admin@sitio.com','Veterinaria Ochoa')
        con.commit()
        print("Persona insertada correctamente.")
    except pyodbc.Error as e:
        print(f"Error al insertar persona: {e}")
    finally:
        con.close()

def insertarCuenta():
    try:
        con = BDconeccion()
        cursor = con.cursor()
        cursor.execute("""IF NOT EXISTS (SELECT 1 FROM USUARIOS WHERE USUARIO LIKE 'ADMIN')
                            BEGIN
                                INSERT INTO USUARIOS (USUARIO,CONTRASEÑA,PERSONA_IDU) 
                                VALUES (?, ?, ?)
                            END""", 'ADMIN', generate_password_hash('Belen123'), 1)
        con.commit()
        print("Cuenta insertada correctamente.")
    except pyodbc.Error as e:
        print(f"Error al insertar cuenta: {e}")
    finally:
        con.close()

def insertarRoles():
    try:
        con = BDconeccion()
        cursor = con.cursor()
        cursor.execute("""  DECLARE @nombreUsuario NVARCHAR(50);
                            SELECT @nombreUsuario = ID_USUARIOS
                            FROM USUARIOS
                            WHERE USUARIO like 'admin';
                            IF NOT EXISTS (SELECT 1 FROM ROLES WHERE ROLES = 'ADMIN')
                            BEGIN
                                INSERT INTO ROLES (ROLES, USUARIO_IDR)
                                VALUES ('ADMIN', @nombreUsuario);  -- Ajusta el ID si necesitas asociarlo a un usuario específico
                            END

                            -- Insertar VETERINARIO si no existe
                            IF NOT EXISTS (SELECT 1 FROM ROLES WHERE ROLES = 'VETERINARIO')
                            BEGIN
                                INSERT INTO ROLES (ROLES, USUARIO_IDR)
                                VALUES ('VETERINARIO', @nombreUsuario);
                            END

                            -- Insertar RECEPCIONISTA si no existe
                            IF NOT EXISTS (SELECT 1 FROM ROLES WHERE ROLES = 'RECEPCIONISTA')
                            BEGIN
                                INSERT INTO ROLES (ROLES, USUARIO_IDR)
                                VALUES ('RECEPCIONISTA', @nombreUsuario);
                            END """)
        con.commit()
        print("Rol insertado correctamente.")
    except pyodbc.Error as e:
        print(f"Error al insertar rol: {e}")
    finally:
        con.close()
insertarPersona()
insertarCuenta()
insertarRoles()