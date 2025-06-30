import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, jsonify, redirect, url_for, send_file
from modulos.helpers import *
from modulos.usuarios import buscarUsuario, rolesPorUsuario
from modulos.razas import  *
from modulos.mascotas import *
from modulos.categoriasprod import *
from modulos.categoriasp import *
from modulos.personas import *
from modulos.propietario import *
from modulos.productos import *
from modulos.ventas import *
from modulos.servicios import *
from modulos.consultas import *
from modulos.coneccion import *
from flask_session import Session
import io
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import urllib.parse
import json


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False #Cierra la sesion despues de 30 días
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#PAGINA PRINCIPAL
@app.route("/")
@login_required
def index():
   return render_template ('index.html')

#LOGIN
@app.route('/login', methods=['GET', 'POST', 'HEAD'])
def login():
    if request.method == 'HEAD':
        return '', 200
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pswd']

        if not username or not password:
            return render_template('login.html', error='Por favor, ingrese usuario y contraseña.')

        from modulos.coneccion import ConnectionManager
        # Ya no se setean credenciales, solo se usa la conexión global
        con = ConnectionManager.get_connection()
        if not con:
            error_msg = ConnectionManager.get_last_error()
            error_msg = error_msg.lower() if error_msg else ""
        
            # Depuración: mostrar el mensaje real de error en consola
            print(f"[DEBUG] Mensaje de error de conexión: '{error_msg}'")
            # Convertir el error a string para asegurar búsquedas correctas
            error_str = str(error_msg).lower() if error_msg else ""
            # Bloqueo de cuenta
            if "locked out" in error_str:
                mensaje = "Tu cuenta ha sido bloqueada por múltiples intentos fallidos. Intenta más tarde o contacta al administrador."
            # Errores de autenticación comunes (contraseña/usuario incorrectos)
            elif any(x in error_str for x in [
                "login failed", "error de inicio de sesión", "authentication failed", "usuario no válido", "18456"
            ]) or error_str.strip() == "":
                mensaje = "Usuario o contraseña incorrectos."
            elif "faltan credenciales" in error_str:
                mensaje = "Debe ingresar usuario y contraseña."
            else:
                mensaje = f"Error al conectar con la base de datos: {error_msg}"

            return render_template('login.html', error=mensaje)

        # Si la conexión fue exitosa, obtiene los roles usando esa conexión
        try:
            cursor = con.cursor()
            cursor.execute("""
                SELECT r.name AS Rol
                FROM sys.database_role_members drm
                JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
                JOIN sys.database_principals u ON drm.member_principal_id = u.principal_id
                WHERE u.name = ?;
            """, username)
            roles = [fila[0] for fila in cursor.fetchall()]
            cursor.close()
        except Exception as e:
            print(f"[DEBUG] Error obteniendo roles: {e}")
            roles = []

        session['user_id'] = username
        session['user_role'] = roles if roles else []
        print('Roles en sesión:', session.get('user_role'))
        return redirect('/')

    elif request.method == 'GET':
        return render_template('login.html')

#CERRAR SESION
@app.route('/logout')
def logout():
      """Log user out."""
      # Forget any user_id
      session.clear()

      # Redirect user to login form
      return redirect("/login")

##################################################################################
#SERVICIOS
@app.route('/servicios')
@login_required
@veterinario_required
def servicios():
   servicios = obtener_servicios()  # Función que obtiene los servicios de la base de datos
   return render_template ('servicios.html', servi = servicios)

#AGREGAR UN NUEVO SERVICIO
@app.route('/agregarservicio', methods=['GET', 'POST'])
@login_required
@admin_required
def agregarservicios():
    if request.method == "POST":
        nombre_servicio = request.form.get("nombres")
        precio_servicio = request.form.get("precios")
        descripcion_servicio = request.form.get("descrips")
        file = request.files.get("imagenurl")

        # VALIDACIONES DE LONGITUD Y CAMPOS
        erroresS = []
        if not nombre_servicio or len(nombre_servicio) > 100:
            erroresS.append("El nombre del servicio es obligatorio y no puede tener más de 100 caracteres.")
        if not precio_servicio:
            erroresS.append("El precio del servicio es obligatorio y debe ser un número positivo.")
        if not descripcion_servicio or len(descripcion_servicio) > 500:
            erroresS.append("La descripción es obligatoria y no puede tener más de 500 caracteres.")
        if file and not allowed_file(file.filename):
            erroresS.append("El archivo de imagen debe ser PNG, JPG o JPEG.")
        # Si hay errores, volver al formulario con mensajes
        if erroresS:
            return render_template('agregarservicio.html', errores=erroresS)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            imagen_url = f"{UPLOAD_FOLDER}/{filename}"
        else:
            imagen_url = None

        print(nombre_servicio, imagen_url, precio_servicio, descripcion_servicio, file)
        insertarserviciocatalogo(nombre_servicio, imagen_url, precio_servicio, descripcion_servicio)
        return redirect('/servicios')

    return render_template('agregarservicio.html')

#BUSCA MASCOTA
@app.route('/buscar_mascota')
@login_required
@vetRec_required
def buscar_mascota():
    q = request.args.get('q', '')
    mascotas = []
    if q:
        from modulos.coneccion import ConnectionManager
        con_local = ConnectionManager.get_connection()
        if not con_local:
            return jsonify([])
        cursor = con_local.cursor()
        cursor.execute("""
            SELECT m.ID_MASCOTA, m.NOMBRE_MASCOTA, m.EDAD, m.PESO, e.NOMBRE_ESPECIE, r.NOMBRE_RAZA, p.nombre, p.apellido
            FROM MASCOTA m
            LEFT JOIN RAZA r ON m.RAZA_ID = r.ID_RAZA
            LEFT JOIN ESPECIE e ON r.ESPECIE_ID = e.ID_ESPECIE
            LEFT JOIN propietario prop ON m.PROPIETARIO_ID = prop.id_propietario
            LEFT JOIN persona p ON prop.persona_id = p.id_persona
            WHERE m.NOMBRE_MASCOTA LIKE ?
        """, ('%' + q + '%',))
        mascotas = [
            {
                'id': row[0],
                'nombre': row[1],
                'edad': row[2],
                'peso': row[3],
                'especie': row[4],
                'raza': row[5],
                'propietario': f"{row[6] or ''} {row[7] or ''}".strip()
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
    return jsonify(mascotas)

#HACE UN SERVICIO A UNA MASCOTA
@app.route('/realizarservicio', methods=["GET", "POST"])
@login_required
@veterinario_required
def realizarservicio():
    if request.method == "GET":
        servicio = mostrarservicio()  # Lista de servicios tipo [(id, nombre, precio)]

        # Construir diccionario {id: precio} para el JS
        servicios_dict = {str(s[0]): s[2] for s in servicio}  # Asegúrate que s[2] es el precio
        servicios_json = json.dumps(servicios_dict)

        return render_template('realizarservicio.html',
                               servic=servicio,
                               serviciosCatalogo=servicios_json)

    elif request.method == "POST":
        fecha = request.form.get("fecs")
        total = request.form.get("tots")
        mascota_id = request.form.get("mascota_id")

        servicio_id = insertar_servicio(fecha, total, mascota_id)

        servicios = request.form.getlist("servicio_id[]")
        precios = request.form.getlist("precio[]")

        for s_id, precio in zip(servicios, precios):
            insertar_detalle_servicio(servicio_id, s_id, precio)

        return redirect('/servicios')

@app.route('/servicios/editar/<int:idservicio>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_servicio(idservicio):
    if request.method == 'POST':
        precio = request.form.get('precio')
        estado = request.form.get('estado')
        if not precio or not estado:
            servicio = obtener_servicio(idservicio)
            error = 'Todos los campos son obligatorios.'
            return render_template('editarservicio.html', servicio=servicio, error=error)
        try:
            actualizar_servicio(idservicio, precio, estado)
            return redirect('/servicios')
        except Exception as e:
            servicio = obtener_servicio(idservicio)
            error = f'Error al actualizar: {e}'
            return render_template('editarservicio.html', servicio=servicio, error=error)
    else:
        servicio = obtener_servicio(idservicio)
        if not servicio:
            return 'Servicio no encontrado', 404
        return render_template('editarservicio.html', servicio=servicio)

#HISTORIAL DE SERVICIOS
@app.route('/historialservicios')
@login_required
@vetRec_required
def historialservicios():
    historial = mostrar_servicios()  # Función que obtiene el historial de servicios
    return render_template('historialservicios.html', historial=historial)

###############################################################
#MASCOTAS
@app.route('/mascotas')
@login_required
@vetRec_required
def mascotas():
    mascotas = mostrarmacota()
    return render_template('mascotas.html', Mascot=mascotas)

#EDITAR MASCOTA
@app.route('/mascotas/editar/<int:idmascota>', methods=["GET", "POST"])
@login_required
@admin_required
def editar_mascota(idmascota):
    if request.method == "POST":
        edad = request.form.get("edad")
        peso = request.form.get("peso")
        propietario_id = int(request.form.get("propietario_id"))
        actualizar_mascota(idmascota, edad, peso, propietario_id)
        return redirect('/mascotas')
    else:
        mascota = mostrarmacota(idmascota)[0]
        print("mascota[5]:", mascota[5], type(mascota[5]))
        razas = mostrarraza_todas()  # Si tu template lo necesita
        propietarios = mostrarpropietarios()
        return render_template("editarmascotas.html", mascota=mascota, razas=razas, propietarios=propietarios)

#FORMULARIO MASCOTA
@app.route('/agregarmascotas', methods=["GET","POST"])
@login_required
@vetRec_required
def agregarmascotas():
    if request.method == "GET":
        especie = mostrarespecie()
        return render_template('agregarmascotas.html', espe=especie)
    elif request.method == "POST":
        Nombremascota = request.form.get("nombrem")
        Edad = request.form.get("edadm")
        Peso = request.form.get("pesom")
        Sexo = request.form.get("sexom")
        Raza = request.form.get("razam")
        propietario_id = request.form.get("propietario_id")

        # VALIDACIONES DE LONGITUD Y CAMPOS
        erroresM = []
        if not Nombremascota or len(Nombremascota) > 30:
            erroresM.append("El nombre de la mascota es obligatorio y no puede tener más de 30 caracteres.")
        if not Edad or not Edad.isdigit() or int(Edad) < 0:
            erroresM.append("La edad de la mascota es obligatoria y debe ser un número positivo.")
        if not Peso or not Peso.replace('.', '', 1).isdigit() or float(Peso) <= 0:
            erroresM.append("El peso de la mascota es obligatorio y debe ser un número positivo.")
        if Sexo not in ['M', 'F']:
            erroresM.append("El sexo de la mascota debe ser 'M' o 'F'.")
        if not Raza:
            erroresM.append("La raza de la mascota es obligatoria.")
        if not propietario_id:
            erroresM.append("Debe seleccionar un propietario para la mascota.")
        if erroresM:
            especie = mostrarespecie()
            return render_template("agregarmascotas.html", errores=erroresM, espe=especie)

        # Insertar la mascota y obtener el ID
        mascota_id = insertarmascota(Nombremascota, Edad, Peso, Sexo, Raza, propietario_id)
        return redirect('/mascotas')


#RAZAS Y ESPECIES
@app.route('/razas/<int:especie_id>', methods=['GET'])
@login_required
@vetRec_required
def razas(especie_id):
    # Obtén las razas asociados a la especie dada
   razas = mostrarraza(especie_id)  # Función que consulta las razas por especie
    # Convertir la lista de tuplas a diccionarios
   razas_dict = [{'id': razas[0], 'nombre': razas[1]} for razas in razas]
    # Devolvemos la lista de razas como un JSON
   return jsonify(razas_dict)

#MOSTRAR PROPIETARIOS para mascotas nuevas
@app.route('/buscar_propietario')
@login_required
@vetRec_required
def buscar_propietario():
    from modulos.coneccion import ConnectionManager
    con_local = ConnectionManager.get_connection()
    if not con_local:
        return jsonify([])
    correo = request.args.get('correo', '').lower().strip()
    cursor = con_local.cursor()
    cursor.execute("""
        SELECT prop.id_propietario, per.nombre, per.apellido, per.cedula, per.telefono, per.correo, per.direccion
        FROM persona AS per
        INNER JOIN propietario AS prop ON per.id_persona = prop.persona_id
        WHERE LOWER(per.correo) LIKE ?
    """, ('%' + correo + '%',))
    propietarios = [
        {
            'id': row[0],
            'nombre': row[1],
            'apellido': row[2],
            'cedula': row[3],
            'telefono': row[4],
            'correo': row[5],
            'direccion': row[6]
        }
        for row in cursor.fetchall()
    ]
    cursor.close()
    return jsonify(propietarios)

@app.route('/obtener_propietario')
@login_required
@vetRec_required
def obtener_propietario():
    correo = request.args.get('correo')
    if not correo:
        return jsonify({'error': 'Falta el correo'}), 400
    prop = buscarpropietario_por_correo(correo)
    if prop:
        return jsonify({
            'nombre': prop[0],
            'apellido': prop[1],
            'cedula': prop[2],
            'telefono': prop[3],
            'correo': prop[4],
            'direccion': prop[5]
        })
    else:
        return jsonify({'error': 'No encontrado'}), 404

###########################################################################
#EMPLEADOS
@app.route('/empleados')
@login_required
def empleados():
   return render_template ('empleados.html')

@app.route('/agregarempleados')
@login_required
def agregarempleados():
   return render_template ('agregarempleados.html')

############################################################################
#CONSULTAS
@app.route('/consultas')
@login_required
@veterinario_required
def consultas():
    consultas = mostrar_consultas()  # Función que obtiene las consultas de la base de datos
    return render_template ('consultas.html', consultas=consultas)

#AGREGAR CONSULTAS
@app.route('/agregarconsultas', methods=['GET', 'POST'])
@login_required
@veterinario_required
def agregarconsultas():
    if request.method == 'POST':
        # Recibe datos del formulario
        fecha = request.form.get('fecc')
        descripcion = request.form.get('dec')
        diagnostico = request.form.get('dic')
        tratamiento = request.form.get('tra')
        precio_consulta = request.form.get('prec')
        mascota_id = request.form.get('mascota_id')

        # Medicamentos (pueden venir como listas)
        medicamentos_id = request.form.getlist('medicamento_id[]')
        dosis = request.form.getlist('dosis[]')
        duracion = request.form.getlist('duracion[]')

        # VALIDACIONES DE LONGITUD Y CAMPOS
        erroresC = []
        if not fecha:
            erroresC.append("La fecha de la consulta es obligatoria.")
        if not descripcion or len(descripcion) > 500:
            erroresC.append("La descripción es obligatoria y no puede tener más de 500 caracteres.")
        if not diagnostico or len(diagnostico) > 500:
            erroresC.append("El diagnóstico es obligatorio y no puede tener más de 500 caracteres.")
        if not tratamiento or len(tratamiento) > 500:
            erroresC.append("El tratamiento es obligatorio y no puede tener más de 500 caracteres.")
        if not precio_consulta:
            erroresC.append("El precio de la consulta es obligatorio y debe ser un número positivo.")
        if not mascota_id:
            erroresC.append("Debe seleccionar una mascota para la consulta.")
        # Validar medicamentos si se envían
        if medicamentos_id:
            if not (len(medicamentos_id) == len(dosis) == len(duracion)):
                erroresC.append("Debe completar dosis y duración para cada medicamento.")
            for d in dosis:
                if not d:
                    erroresC.append("La dosis de cada medicamento es obligatoria.")
            for du in duracion:
                if not du:
                    erroresC.append("La duración de cada medicamento es obligatoria.")
        # Si hay errores, volver al formulario con mensajes
        if erroresC:
            return render_template('agregarconsultas.html', errores=erroresC)

        # Inserta la consulta y obtiene el ID generado
        consulta_id = insertarconsulta(fecha, descripcion, diagnostico, tratamiento, float(precio_consulta or 0), mascota_id)

        # Inserta los medicamentos asociados
        for i in range(len(medicamentos_id)):
            insertar_consulta_medicamento(
                consulta_id,
                medicamentos_id[i],
                dosis[i],
                duracion[i]
            )

        return redirect(url_for('consultas'))

    # Si es GET, solo muestra el formulario
    return render_template('agregarconsultas.html')

#TABLA DE MASCOTAS PARA LA CONSULTA
# TABLA DE MASCOTAS PARA LA CONSULTA
@app.route('/buscar_mascotas_consulta')
@login_required
@vetRec_required
def buscar_mascotaconsulta():
    try:
        q = request.args.get('q', '')
        consultamascotas = []
        if q:
            from modulos.coneccion import ConnectionManager
            con_local = ConnectionManager.get_connection()
            if not con_local:
                return jsonify([])

            cursor = con_local.cursor()
            cursor.execute("""
                SELECT m.ID_MASCOTA, m.NOMBRE_MASCOTA, m.EDAD, m.PESO, e.NOMBRE_ESPECIE, r.NOMBRE_RAZA, p.nombre, p.apellido
                FROM MASCOTA m
                LEFT JOIN RAZA r ON m.RAZA_ID = r.ID_RAZA
                LEFT JOIN ESPECIE e ON r.ESPECIE_ID = e.ID_ESPECIE
                LEFT JOIN propietario prop ON m.PROPIETARIO_ID = prop.id_propietario
                LEFT JOIN persona p ON prop.persona_id = p.id_persona
                WHERE m.NOMBRE_MASCOTA LIKE ?
            """, ('%' + q + '%',))

            filas = cursor.fetchall()
            consultamascotas = [
                {
                    'id': row[0],
                    'nombre': row[1],
                    'edad': row[2],
                    'peso': row[3],
                    'especie': row[4],
                    'raza': row[5],
                    'propietario': f"{row[6] or ''} {row[7] or ''}".strip()
                }
                for row in filas
            ]
            cursor.close()

        return jsonify(consultamascotas)
    
    except Exception as e:
        # Mostralo en consola para debugging
        print(f"Error en /buscar_mascotas_consulta: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


#BUSCAR MEDICAMENTO
# Esta ruta se usa para buscar medicamentos por nombre e devolver sugerencias
@app.route('/buscar_medicamento')
@login_required
@veterinario_required
def buscar_medicamento():
    query = request.args.get('q', '').lower().strip()
    medicamentos = obtener_medicamentos()

    sugerencias = [
        {
            'id': m[0],
            'nombre': m[1],
            'precio': float(m[2])  # Ahora sí estará en la posición 2
        }
        for m in medicamentos
        if query in m[1].lower()
    ]
    return jsonify(sugerencias)

###########################################################################
#PROVEEDORES
# @app.route('/proveedores')
# @login_required
# def proveedores():
#    return render_template ('proveedores.html')

############################################################################
#PROPIETARIOS
@app.route('/propietarios')
@login_required
@vetRec_required
def propietarios():
   return render_template ('propietarios.html')

#FORMULARIO PROPIETARIO
@app.route('/agregarpropietario', methods=["GET", "POST"])
@login_required
@vetRec_required
def agregarpropietario():
    if request.method == "GET":
        categorias = mostrarcategoriasp()
        return render_template("agregarpropietario.html", categ=categorias)
    elif request.method == "POST":
        # Datos de la persona
        nombre = request.form.get("nombrep")
        apellido = request.form.get("apellidop")
        cedula = request.form.get("cedp")
        telefono = request.form.get("telp")
        correo = request.form.get("corp")
        direccion = request.form.get("dirp")
        tipo = request.form.get("tipop")  # ID del tipo cliente
        estado = request.form.get("estadop")  # Estado del propietario

        # VALIDACIONES DE LONGITUD Y CAMPOS
        erroresP = []
        if not nombre or len(nombre) > 50:
            erroresP.append("Los nombre son obligatorio y no puede tener más de 50 caracteres.")
        if not apellido or len(apellido) > 50:
            erroresP.append("Los apellido son obligatorio y no puede tener más de 50 caracteres.")
        if not cedula or len(cedula) > 16:
            erroresP.append("La cédula es obligatoria y no puede tener más de 16 caracteres.")
        if not telefono or len(telefono) > 8:
            erroresP.append("El teléfono es obligatorio y no puede tener más de 20 caracteres.")
        if not correo or len(correo) > 100:
            erroresP.append("El correo es obligatorio y no puede tener más de 100 caracteres.")
        if not direccion or len(direccion) > 700:
            erroresP.append("La dirección es obligatoria y no puede tener más de 700 caracteres.")
        if not tipo:
            erroresP.append("Debe seleccionar un tipo de cliente.")
        if not estado:
            erroresP.append("Debe seleccionar el estado del propietario.")
        if erroresP:
            categorias = mostrarcategoriasp()
            return render_template("agregarpropietario.html", errores=erroresP, categ=categorias)

        print("Datos recibidos:", nombre, apellido, cedula, telefono, correo, direccion, tipo, estado)

        # Verificar conexión antes de insertar persona
        from modulos.coneccion import ConnectionManager
        con = ConnectionManager.get_connection()
        if not con:
            erroresP.append("No se pudo conectar a la base de datos. Verifique sus credenciales o conexión.")
            categorias = mostrarcategoriasp()
            return render_template("agregarpropietario.html", errores=erroresP, categ=categorias)

        persona_id = insertarpersona(nombre, apellido, cedula, telefono, correo, direccion)

        if persona_id:
            try:
                insertarpropietario(persona_id, tipo, estado)  # No se asocia mascota aquí
                return redirect('/mascotas')
            except Exception as e:
                print("Error en insertarpropietario:", e)
                import traceback
                traceback.print_exc()
                erroresP.append(f"Error al insertar propietario: {e}")
                categorias = mostrarcategoriasp()
                return render_template("agregarpropietario.html", errores=erroresP, categ=categorias)
        else:
            erroresP.append("Error: no se pudo insertar el propietario (persona no creada)")
            categorias = mostrarcategoriasp()
            return render_template("agregarpropietario.html", errores=erroresP, categ=categorias)

#CATEGORIAS CLIENTE
@app.route('/tiposclientes', methods=['GET'])
@login_required
@vetRec_required
def tiposclientes():
    categorias = mostrarcategoriasp()  # [(id, nombre), ...]
    categorias_dict = [{'id': c[0], 'nombre': c[1]} for c in categorias]
    return jsonify(categorias_dict)

#######################################################################
#CATEGORIAS PRODUCTOS
UPLOAD_FOLDER = 'static/assets/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#PRODUCTOS
@app.route('/productos')
@login_required
@vetRec_required
def productos():
     lista_productos = obtener_productos()
     return render_template ('productos.html', productos=lista_productos)

#AGREGAR AL INVENTARIO UN NUEVO PRODUCTO
@app.route('/compra', methods=['GET', 'POST'])
@login_required
@admin_required
def compra():
    if request.method == "POST":
        nombre = request.form.get("nombrep")
        descripcion = request.form.get("descripp")
        precio = request.form.get("preciop")
        tipo_venta = request.form.get("tipo_venta")
        categoria = request.form.get("categoria")
        file = request.files.get("imagenurl")

        # Obtener precio_unitario del formulario
        precio_unitario = request.form.get("precio_unitario", 0)
        try:
            precio_unitario = float(precio_unitario)
        except (ValueError, TypeError):
            precio_unitario = 0

        # VALIDACIONES DE LONGITUD Y CAMPOS
        erroresProd = []
        if not nombre or len(nombre) > 50:
            erroresProd.append("El nombre del producto es obligatorio y no puede tener más de 50 caracteres.")
        if not descripcion or len(descripcion) > 300:
            erroresProd.append("La descripción es obligatoria y no puede tener más de 300 caracteres.")
        if not precio:
            erroresProd.append("El precio es obligatorio y debe ser un número positivo.")
        if not tipo_venta:
            erroresProd.append("Debe seleccionar el tipo de venta.")
        if not categoria:
            erroresProd.append("Debe seleccionar una categoría.")
        if file and not allowed_file(file.filename):
            erroresProd.append("El archivo de imagen debe ser PNG, JPG o JPEG.")
        # Validar stock y peso según tipo de venta
        stock_unidades = request.form.get("unidadesp", 0)
        try:
            stock_unidades = int(stock_unidades)
        except (ValueError, TypeError):
            stock_unidades = 0
        if stock_unidades < 0:
            erroresProd.append("Las unidades deben ser un número positivo.")

        if tipo_venta == "unidad":
            peso_por_unidad = 0
            stock_peso = 0
            precio_unitario = 0
        else:  # tipo_venta == "peso"
            peso_por_unidad = request.form.get("pesop", None)
            stock_peso = request.form.get("stockpesop", None)
            precio_unitario = request.form.get("precio_unitario", None)
            # Validar que los campos no sean vacíos ni cero
            if not peso_por_unidad or not str(peso_por_unidad).replace('.', '', 1).isdigit() or float(peso_por_unidad) <= 0:
                erroresProd.append("El peso por unidad es obligatorio y debe ser un número positivo.")
            else:
                peso_por_unidad = float(peso_por_unidad)
            if not stock_peso or not str(stock_peso).replace('.', '', 1).isdigit() or float(stock_peso) <= 0:
                erroresProd.append("El stock total en peso es obligatorio y debe ser un número positivo.")
            else:
                stock_peso = float(stock_peso)
            if not precio_unitario or not str(precio_unitario).replace('.', '', 1).isdigit() or float(precio_unitario) <= 0:
                erroresProd.append("El precio por kilo es obligatorio y debe ser un número positivo.")
            else:
                precio_unitario = float(precio_unitario)
        if erroresProd:
            categ = mostrarcategoria()
            return render_template('compra.html', errores=erroresProd, categ=categ)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            imagen_url = f"{UPLOAD_FOLDER}/{filename}"
        else:
            imagen_url = None

        print(nombre, imagen_url, descripcion, precio, precio_unitario, stock_unidades, peso_por_unidad, stock_peso, tipo_venta, categoria)
        insertarproducto(
            nombre,
            imagen_url,
            descripcion,
            precio,
            precio_unitario,
            stock_unidades,
            peso_por_unidad,
            stock_peso,
            tipo_venta,
            categoria
        )
        return redirect('/productos')

    categ = mostrarcategoria()
    return render_template('compra.html', categ=categ)

#EDITAR PRODUCTO
@app.route('/productos/editar/<int:idproducto>', methods=["GET", "POST"])
@login_required
@admin_required
def editar_producto(idproducto):
    if request.method == "POST":
        producto = obtenerunproducto(idproducto)
        tipo_venta = producto[9]
        estado = request.form.get("estado", "activo")
        if tipo_venta == "unidad":
            precio = request.form.get("preciop")
            unidades_actuales = producto[6] or 0
            unidades_agregar = int(request.form.get("unidades_agregar", 0))
            stock_unidades = int(unidades_actuales) + unidades_agregar
            precio_unitario = 0
            peso_por_unidad = 0
            stock_peso = 0
        else:
            precio = request.form.get("precio_kg")
            precio_unitario = request.form.get("precio_unitario")
            unidades_actuales = producto[6] or 0
            unidades_agregar = int(request.form.get("unidades_agregar", 0))
            stock_unidades = int(unidades_actuales) + unidades_agregar
            peso_por_unidad = producto[7] or 0
            # Calcular el nuevo stock_peso sumando el peso de las nuevas unidades
            stock_peso_actual = producto[8] or 0
            stock_peso = float(stock_peso_actual) + (unidades_agregar * float(peso_por_unidad))
        actualizar_producto(
            idproducto,
            precio,
            precio_unitario,
            stock_unidades,
            peso_por_unidad,
            stock_peso,
            tipo_venta,
            estado
        )
        return redirect('/productos')
    else:
        producto = obtenerunproducto(idproducto)  # Usa la función que trae un solo producto
        return render_template("editaproducto.html", producto=producto)

#BUSCAR PRODUCTO
@app.route('/buscar_producto')
@login_required
@vetRec_required  # Este decorador ya permite todos los roles de ventas, lo dejamos comentado para claridad

def buscar_producto():
    q = request.args.get('q', '')
    productos = []
    if q:
        con = ConnectionManager.get_connection()
        cursor = con.cursor()
        cursor.execute("""
            SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, PRECIO_PRODUCTO, PRECIO_UNITARIO, STOCK_UNIDADES, STOCK_PESO, TIPO_VENTA
            FROM PRODUCTO
            WHERE NOMBRE_PRODUCTO LIKE ?
            """, ('%' + q + '%',))
        productos = [
            {
                'id': row[0],
                'nombre': row[1],
                'precio': float(row[2]),
                'precio_unitario': float(row[3]),
                'stock_unidades': int(row[4]),
                'stock_peso': float(row[5]),
                'tipo_venta': row[6]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
    return jsonify(productos)

###############################################################
#VENTAS
@app.route('/ventas')
@login_required
@vetRec_required
def ventas():
   productos = obtener_productos()
   return render_template ('ventas.html', productos=productos )

#REALIZAR VENTA
@app.route('/realizar_venta', methods=['POST'])
@login_required
@vetRec_required
def realizar_venta():
    productos = request.form.getlist('producto_id')
    cantidades_libras = request.form.getlist('cantidad')
    precios_unitarios = request.form.getlist('precio_unitario')
    tipos_venta = request.form.getlist('tipo_venta')
    cantidades_kg = request.form.getlist('cantidad_kg')
    fecha_venta = request.form.get('fev')
    persona_id = request.form.get('persona_id')  # <-- Cambiado para asociar a la persona seleccionada
    total_venta = 0

    # VALIDACIONES DE LONGITUD Y CAMPOS
    erroresV = []
    if not productos or not all(productos):
        erroresV.append("Debe seleccionar al menos un producto para la venta.")
    if not cantidades_libras or not all(cantidades_libras):
        erroresV.append("Debe ingresar la cantidad para cada producto.")
    if not precios_unitarios or not all(precios_unitarios):
        erroresV.append("Debe ingresar el precio unitario para cada producto.")
    if not tipos_venta or not all(tipos_venta):
        erroresV.append("Debe seleccionar el tipo de venta para cada producto.")
    if not fecha_venta:
        erroresV.append("La fecha de la venta es obligatoria.")
    # Validar cantidades y precios positivos
    for i, cantidad in enumerate(cantidades_libras):
        try:
            cant = float(cantidad)
            if cant <= 0:
                erroresV.append(f"La cantidad del producto {i+1} debe ser un número positivo.")
        except (ValueError, TypeError):
            erroresV.append(f"La cantidad del producto {i+1} no es válida.")
    for i, precio in enumerate(precios_unitarios):
        try:
            prec = float(precio)
            if prec <= 0:
                erroresV.append(f"El precio unitario del producto {i+1} debe ser un número positivo.")
        except (ValueError, TypeError):
            erroresV.append(f"El precio unitario del producto {i+1} no es válido.")
    # Si hay errores, volver al formulario con mensajes
    if erroresV:
        productos_lista = obtener_productos()
        return render_template('ventas.html', errores=erroresV, productos=productos_lista)

    # Validación de stock
    for i, producto_id in enumerate(productos):
        tipo_venta = tipos_venta[i]
        producto_id_int = int(producto_id)

        if tipo_venta == 'unidad':
            cantidad = int(float(cantidades_libras[i]))
            stock = obtener_stock_unidades(producto_id_int)
            if cantidad > stock:
                return f"No hay suficientes unidades para el producto {producto_id}", 400
        else:  # tipo_venta == 'peso'
            cantidad_libras = float(cantidades_kg[i])  # O cantidades_libras[i] (ambos traen lo mismo)
            cantidad_kg = cantidad_libras * 0.453592  # Convertimos a kg
            stock_kg = obtener_stock_peso(producto_id_int)
            if cantidad_kg > stock_kg:
                return f"No hay suficiente peso (kg) para el producto {producto_id}", 400

    # Calcular total y registrar venta
    for i in range(len(productos)):
        tipo_venta = tipos_venta[i]
        precio_unitario = float(precios_unitarios[i])

        if tipo_venta == 'unidad':
            cantidad = int(float(cantidades_libras[i]))
            subtotal = precio_unitario * cantidad
        else:
            cantidad_libras = float(cantidades_kg[i])
            cantidad_kg = cantidad_libras * 0.453592
            subtotal = precio_unitario * cantidad_kg

        total_venta += subtotal

    venta_id = insertar_venta(fecha_venta, total_venta, persona_id)
    # Guardar detalle y descontar stock
    for i in range(len(productos)):
        producto_id = int(productos[i])
        tipo_venta = tipos_venta[i]
        precio_unitario = float(precios_unitarios[i])

        if tipo_venta == 'unidad':
            cantidad = int(float(cantidades_libras[i]))
            subtotal = precio_unitario * cantidad
            insertar_detalle_venta(venta_id, producto_id, cantidad, subtotal)
            descontar_stock(producto_id, cantidad)  # unidades
        else:
            cantidad_libras = float(cantidades_kg[i])
            cantidad_kg = cantidad_libras * 0.453592
            subtotal = precio_unitario * cantidad_kg
            insertar_detalle_venta(venta_id, producto_id, cantidad_kg, subtotal)
            descontar_stock(producto_id, cantidad_kg)  # kilos

    return redirect('/productos')


@app.route('/buscar_persona')
@login_required
@vetRec_required

def buscar_persona():
    q = request.args.get('q', '').strip().lower()
    personas = []
    if q:
        con = ConnectionManager.get_connection()
        cursor = con.cursor()
        cursor.execute('''
            SELECT id_persona, nombre, apellido, cedula, telefono, correo, direccion
            FROM persona
            WHERE LOWER(nombre) LIKE ? OR LOWER(apellido) LIKE ? OR LOWER(correo) LIKE ?
        ''', (f'%{q}%', f'%{q}%', f'%{q}%'))
        personas = [
            {
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'cedula': row[3],
                'telefono': row[4],
                'correo': row[5],
                'direccion': row[6]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
    return jsonify(personas)


#########################################################################
# REPORTES
@app.route('/reporte_mascotas_pdf')
def reporte_mascotas_pdf():
    mascotas = mostrarmacota()
    columnas = [
        "Nombre", "Edad", "Peso", "Sexo", "Raza", "Propietario",
        "Cédula", "Teléfono", "Correo", "Dirección", "Estado"
    ]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    data = [columnas] + [list(m[:-1]) for m in mascotas]  # Quitar el ID para el PDF
    styles = getSampleStyleSheet()

    # Crear el título del reporte
    titulo = Paragraph("Reporte de Mascotas", styles['Title'])
    espacio = Spacer(1, 12)
    table = Table(data)

    style = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)

    elements = [titulo, espacio, table]
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_mascotas.pdf", mimetype='application/pdf')


@app.context_processor
def inject_mensaje_whatsapp():
    try:
        con = ConnectionManager.get_connection()
        if con is None:
            raise Exception("No se pudo obtener la conexión a la base de datos")
        cursor = con.cursor()
        cursor.execute('SELECT nombre_mascota, edad, sexo, raza FROM mascotas_vista LIMIT 5')
        mascotas = cursor.fetchall()
        cursor.close()
        con.close()
    except Exception as e:
        print("Error al obtener mascotas:", e)
        mascotas = []

    mensaje = " Reporte de mascotas:\n"
    for m in mascotas:
        mensaje += f"- {m[0]}, {m[1]} años, {m[2]}, raza {m[3]}\n"
    return dict(mensaje_whatsapp=mensaje)


@app.route('/reporte_ventas_pdf')
def reporte_ventas_pdf():
    ventas = mostrar_ventas()
    columnas = [
        "ID Venta", "Fecha", "Nombre", "Apellido", "Producto",
        "Cantidad", "Tipo Venta", "Precio", "Total"
    ]

    # Generar PDF en memoria
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    # Crear el título del reporte
    titulo = Paragraph("Reporte de Ventas", styles['Title'])
    espacio = Spacer(1, 12)
    # Armar datos para la tabla, primera fila columnas + datos ventas
    data = [columnas] + [list(map(str, v)) for v in ventas]

    table = Table(data)

    style = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)

    elements = [titulo, espacio, table]
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_ventas.pdf", mimetype='application/pdf')

# Context processor para generar mensaje de WhatsApp con resumen de ventas recientes
@app.context_processor
def inject_mensaje_ventas_whatsapp():
    try:
        ventas = mostrar_ventas()
    except Exception as e:
        ventas = []

    mensaje = "🛒 Últimas ventas:\n"
    for v in ventas[:5]:  # solo 5 últimas para no saturar
        mensaje += f"- {v[1]}: {v[4]} x {v[5]} ({v[6]}), Total: {v[8]}\n"

    return dict(mensaje_ventas_whatsapp=mensaje)


@app.route('/reporte_servicios_pdf')
def reporte_servicios_pdf():
    servicios = mostrar_servicios()  # Usa tu función existente
    columnas = ["Mascota", "Fecha", "Servicio", "Descripción", "Total"]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Convertir todos los datos a string para evitar errores en ReportLab
    data = [columnas] + [list(map(str, s)) for s in servicios]
    styles = getSampleStyleSheet()

    # Crear el título del reporte
    titulo = Paragraph("Reporte de Servicios", styles['Title'])
    espacio = Spacer(1, 12)
    table = Table(data)

    style = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)

    elements = [titulo, espacio, table]
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_servicios.pdf", mimetype='application/pdf')

@app.context_processor
def inject_mensaje_servicios_whatsapp():
    try:
        servicios = mostrar_servicios()
    except Exception:
        servicios = []

    mensaje = "🛎️ Últimos servicios realizados:\n"
    for s in servicios[:5]:  # Mostrar solo los últimos 5 servicios
        mensaje += f"- {s[1]}: {s[2]} para {s[0]}, Total: {s[4]}\n"

    return dict(mensaje_servicios_whatsapp=mensaje)

@app.route('/reporte_consultas_pdf')
def reporte_consultas_pdf():
    consultas = mostrar_consultas()
    columnas = [
        "Mascota", "Peso", "Edad", "Fecha", "Descripcion", "Total"
    ]

    buffer = io.BytesIO()
    columnas = ['Mascota', 'Peso', 'Edad', 'Fecha', 'Descripción', 'Total']
    data = [columnas] + [
        [c['mascota'], c['peso'], c['edad'], c['fecha'], c['descripcion'], f"C$ {c['total']}"]
        for c in consultas
    ]
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    # Crear el título del reporte
    titulo = Paragraph("Reporte de Consultas", styles['Title'])
    espacio = Spacer(1, 12)
    table = Table(data)

    style = TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)

    elements = [titulo, espacio, table]
    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="reporte_consultas.pdf", mimetype='application/pdf')


@app.context_processor
def inject_mensaje_consultas_whatsapp():
    try:
        consultas = mostrar_consultas()
    except Exception:
        consultas = []

    mensaje = "🛎️ Últimas consultas realizadas:\n"
    for s in consultas[:5]:  # Mostrar solo las últimas 5
        mensaje += f"- {s['fecha']}: {s['descripcion']} para {s['mascota']}, Total: C$ {s['total']}\n"

    return dict(mensaje_consultas_whatsapp=mensaje)

#HISTORIAL DE VENTAS
@app.route('/historialventas')
@login_required
@vetRec_required
def historial_ventas():
    historial = mostrar_ventas()
    return render_template('historialventas.html', historial=historial)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)