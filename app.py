import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, jsonify, redirect, url_for
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
from flask_session import Session


app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False #Cierra la sesion despues de 30 días
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#pagina principal
@app.route("/")
@login_required
def index():
   return render_template ('index.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pswd']

        if not username or not password:
            return render_template('login.html', error='Por favor, ingrese usuario y contraseña.')

        if buscarUsuario(username, password):
            id_persona = obtener_id_persona(username)  # Debe retornar el ID numérico
            session['user_id'] = id_persona
            print("session['user_id'] =", session['user_id'], type(session['user_id']))
            Rol = rolesPorUsuario(username)
            session['Roles'] = [r[0] for r in Rol] if Rol else None
            return redirect('/')
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos.')

    elif request.method == 'GET':
        return render_template('login.html')

#SERVICIOS
@app.route('/servicios')
@login_required
def servicios():
   servicios = obtener_servicios()  # Función que obtiene los servicios de la base de datos
   return render_template ('servicios.html', servi = servicios)

@app.route('/agregarservicio', methods=['GET', 'POST'])
@login_required
def agregarservicios():
    if request.method == "POST":
        nombre_servicio = request.form.get("nombres")
        precio_servicio = request.form.get("precios")
        descripcion_servicio = request.form.get("descrips") 
        file = request.files.get("imagenurl")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            imagen_url = f"{UPLOAD_FOLDER}/{filename}"
        else:
            imagen_url = None

        print(nombre_servicio, imagen_url, precio_servicio, descripcion_servicio, file) 
        insertar_servicio(nombre_servicio, imagen_url, precio_servicio, descripcion_servicio)
        return redirect('/servicios')
   
    return render_template('agregarservicio.html')

#MASCOTAS
@app.route('/mascotas')
@login_required
def mascotas():
    mascotas = mostrarmacota() 
    return render_template('mascotas.html', Mascot=mascotas)

@app.route('/mascotas/editar/<int:idmascota>', methods=["GET", "POST"])
@login_required
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

#EMPLEADOS
@app.route('/empleados')
@login_required
def empleados():
   return render_template ('empleados.html')

@app.route('/agregarempleados')
@login_required
def agregarempleados():
   return render_template ('agregarempleados.html')

#CONSULTAS
@app.route('/consultas')
@login_required
def consultas():
   return render_template ('consultas.html')

@app.route('/agregarconsultas')
@login_required
def agregarconsultas():
   return render_template ('agregarconsultas.html')

#PROVEEDORES
@app.route('/proveedores')
@login_required
def proveedores():
   return render_template ('proveedores.html')

#PROPIETARIOS
@app.route('/propietarios')
@login_required
def propietarios():
   return render_template ('propietarios.html')

#cerrar sesion
@app.route('/logout')
def logout():
      """Log user out."""
      # Forget any user_id
      session.clear()
   
      # Redirect user to login form
      return redirect("/login")

#FORMULARIO MASCOTA
@app.route('/agregarmascotas', methods=["GET","POST"])
@login_required
@veterinario_required
def agregarmascotas():
   if request.method == "GET":
      especie = mostrarespecie()
      return render_template ('agregarmascotas.html', espe = especie)
   elif request.method == "POST":
      Nombremascota = request.form.get("nombrem")
      Edad = request.form.get("edadm")
      Peso = request.form.get("pesom")
      Sexo = request.form.get("sexom")
      Raza= request.form.get("razam")
      insertarmascota (Nombremascota, Edad, Peso, Sexo, Raza )
      return redirect ('/mascotas')

#RAZAS Y ESPECIES
@app.route('/razas/<int:especie_id>', methods=['GET'])
@login_required
def razas(especie_id):
    # Obtén las razas asociados a la especie dada
   razas = mostrarraza(especie_id)  # Función que consulta las razas por especie
    # Convertir la lista de tuplas a diccionarios
   razas_dict = [{'id': razas[0], 'nombre': razas[1]} for razas in razas]
    # Devolvemos la lista de razas como un JSON
   return jsonify(razas_dict)

#FORMULARIO PROPIETARIO
@app.route('/agregarpropietario', methods=["GET", "POST"])
@login_required
@veterinario_required
def agregarpropietario():
    if request.method == "GET":
        mascotas = mostrartodaslasmascotas()
        categorias = mostrarcategoriasp()
        return render_template("agregarpropietario.html", mascot=mascotas, categ=categorias)
    elif request.method == "POST":
        # Datos de la persona
        nombre = request.form.get("nombrep")
        apellido = request.form.get("apellidop")
        cedula = request.form.get("cedp")
        telefono = request.form.get("telp")
        correo = request.form.get("corp")
        direccion = request.form.get("dirp")
        tipo = request.form.get("tipop")  # ID del tipo cliente
        mascota_id = request.form.get("mascotap")  # ID de mascota
        estado = request.form.get("estadop")  # Estado del propietario

        print("Datos recibidos:", nombre, apellido, cedula, telefono, correo, direccion, tipo, mascota_id, estado)

        persona_id = insertarpersona(nombre, apellido, cedula, telefono, correo, direccion)

        if persona_id and mascota_id:
            insertarpropietario(persona_id, tipo, mascota_id, estado)
            return redirect('/mascotas')
        else:
            return "Error: no se pudo insertar el propietario"


#CATEGORIAS CLIENTE
@app.route('/tiposclientes', methods=['GET'])
@login_required
def tiposclientes():
    categorias = mostrarcategoriasp()  # [(id, nombre), ...]
    categorias_dict = [{'id': c[0], 'nombre': c[1]} for c in categorias]
    return jsonify(categorias_dict)

#CATEGORIAS PRODUCTOS
UPLOAD_FOLDER = 'static/assets/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#PRODUCTOS
@app.route('/productos')
@login_required
@recepcionista_required
def productos():
     lista_productos = obtener_productos()
     return render_template ('productos.html', productos=lista_productos)


@app.route('/compra', methods=['GET', 'POST'])
@login_required
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

        if tipo_venta == "unidad":
            stock_unidades = request.form.get("unidadesp", 0)
            try:
                stock_unidades = int(stock_unidades)
            except (ValueError, TypeError):
                stock_unidades = 0
            peso_por_unidad = 0
            stock_peso = 0
        else:  # tipo_venta == "peso"
            stock_unidades = request.form.get("unidadesp", 0)
            try:
                stock_unidades = int(stock_unidades)
            except (ValueError, TypeError):
                stock_unidades = 0
            peso_por_unidad = request.form.get("pesop", 0)
            stock_peso = request.form.get("stockpesop", 0)
            try:
                peso_por_unidad = float(peso_por_unidad)
            except (ValueError, TypeError):
                peso_por_unidad = 0
            try:
                stock_peso = float(stock_peso)
            except (ValueError, TypeError):
                stock_peso = 0

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
def editar_producto(idproducto):
    if request.method == "POST":
        precio = request.form.get("preciop")
        unidades = request.form.get("unidadesp")
        actualizar_producto(idproducto, precio, unidades)
        return redirect('/productos')
    else:
        producto = obtenerunproducto(idproducto)  # Usa la función que trae un solo producto
        return render_template("editaproducto.html", producto=producto)
    
#BUSCAR PRODUCTO
# filepath: c:\Users\Belen\Desktop\VET\app.py
@app.route('/buscar_producto')
@login_required
def buscar_producto():
    q = request.args.get('q', '')
    productos = []

    print (q)
    if q:
        cursor = con.cursor()
        cursor.execute("""
            SELECT ID_PRODUCTO, NOMBRE_PRODUCTO, PRECIO_PRODUCTO, STOCK_UNIDADES, STOCK_PESO, TIPO_VENTA, PRECIO_UNITARIO
            FROM PRODUCTO
            WHERE NOMBRE_PRODUCTO LIKE ?
            """, ('%' + q + '%',))
        productos = [
            {
                'id': row[0],
                'nombre': row[1],
                'precio': row[2],
                'stock_unidades': row[3],
                'stock_peso': float(row[4]),
                'tipo_venta': row[5],
                'precio_unitario': row[6]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
    return jsonify(productos)

#VENTAS
@app.route('/ventas')
@login_required
def ventas():
   productos = obtener_productos()
   return render_template ('ventas.html', productos=productos )

@app.route('/realizar_venta', methods=['POST'])
@login_required
def realizar_venta():
    productos = request.form.getlist('producto_id')
    cantidades_libras = request.form.getlist('cantidad')  # en libras (si es por peso) o unidades (si es por unidad)
    precios_unitarios = request.form.getlist('precio_unitario')  # en córdobas por kg o por unidad
    tipos_venta = request.form.getlist('tipo_venta')  # 'unidad' o 'peso'
    cantidades_kg = request.form.getlist('cantidad_kg')  # mismo que cantidades_libras (en libras en realidad)
    fecha_venta = request.form.get('fev')
    persona_id = session['user_id']
    total_venta = 0

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

    return redirect('/ventas')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)