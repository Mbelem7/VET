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
@app.route('/login',methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
         username = request.form['user']
         password = request.form['pswd']
         
         if not username or not password:
            return render_template('login.html', error='Por favor, ingrese usuario y contraseña.')

         if buscarUsuario(username, password):
            session['user_id'] = username 
            Rol = rolesPorUsuario(username)
            #Convierte la lista de tuplas de roles, en una lista de strings
            session['Roles'] = [r[0] for r in Rol] if Rol else None
            return redirect('/')
         else:
            return render_template('login.html', error='Usuario o contraseña incorrectos.')


      elif request.method == 'GET':
         return render_template ('login.html')

@app.route('/ventas')
@login_required
def ventas():
   return render_template ('ventas.html')


# @app.route('/compra')
# @login_required
# def compra():
#    return render_template ('compra.html')

@app.route('/servicios')
@login_required
def servicios():
   return render_template ('servicios.html')

@app.route('/agregarservicios')
@login_required
def agregarservicios():
   return render_template ('agregarservicios.html')

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

@app.route('/empleados')
@login_required
def empleados():
   return render_template ('empleados.html')

@app.route('/agregarempleados')
@login_required
def agregarempleados():
   return render_template ('agregarempleados.html')

@app.route('/consultas')
@login_required
def consultas():
   return render_template ('consultas.html')

@app.route('/agregarconsultas')
@login_required
def agregarconsultas():
   return render_template ('agregarconsultas.html')

@app.route('/proveedores')
@login_required
def proveedores():
   return render_template ('proveedores.html')

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
        unidades = request.form.get("unidadesp")
        categoria = request.form.get("categoria")
        file = request.files.get("imagenurl")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            imagen_url = f"{UPLOAD_FOLDER}/{filename}"
        else:
            imagen_url = None
         
        print(nombre, imagen_url, descripcion, precio, unidades, categoria)
        insertarproducto(nombre, imagen_url, descripcion, precio, unidades, categoria)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)