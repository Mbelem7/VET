from flask import Flask, render_template, request, redirect, session, jsonify
from modulos.helpers import *
from modulos.usuarios import buscarUsuario, rolesPorUsuario
from modulos.razas import  *
from modulos.mascotas import *
from modulos.categoriasprod import *
from modulos.categoriasp import *
from modulos.personas import *
from modulos.propietario import * 
from flask_session import Session
import pdfkit
import pandas as pd
from io import BytesIO
from flask import send_file, render_template
from flask import render_template, make_response, url_for

# form modulos.productos import *
from modulos.reportes import obtener_reporte_propietarios
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




@app.route('/productos')
@login_required
@recepcionista_required
def productos():
   return render_template ('productos.html')


@app.route('/ventas')
@login_required
def ventas():
   return render_template ('ventas.html')


@app.route('/compra')
@login_required
def compra():
   return render_template ('compra.html')

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

      print("Datos recibidos:", nombre, apellido, cedula, telefono, correo, direccion, tipo, mascota_id)

      persona_id = insertarpersona(nombre, apellido, cedula, telefono, correo, direccion)

    if persona_id and mascota_id:
        insertarpropietario(persona_id, tipo, mascota_id)
        return redirect('/propietarios')
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
@app.route('/compra', methods=['GET'])
@login_required
def categorias():
   if request.method == "GET":
      categ = mostrarcategoria()
      return render_template ('compra.html', categ = categ)
   
   #  Reportes
@app.route('/reporte/propietarios')
def reporte_propietarios():
    datos = obtener_reporte_propietarios()
    return render_template('reportes_propietarios.html', propietarios=datos)

# Ruta para reporte PDF

@app.route('/reporte/propietarios/pdf')
@app.route('/reporte/propietarios/pdf')
def reporte_propietarios_pdf():
    # Obtener los datos (ajusta esto según tu lógica real)
    datos = obtener_reporte_propietarios()  # <-- asegúrate de tener esta función

    # Renderiza el HTML como string
    rendered = render_template('reportes_propietarios_pdf.html', propietarios=datos)

    # Ruta completa al ejecutable wkhtmltopdf (ajústala si lo tienes en otra carpeta)
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config_pdfkit = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Opciones necesarias para que funcione correctamente en Windows
    options = {
        'enable-local-file-access': None,
        'encoding': 'UTF-8'
    }

    # Generar el PDF
    pdf = pdfkit.from_string(rendered, False, configuration=config_pdfkit, options=options)

    # Preparar respuesta HTTP con PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_propietarios.pdf'
    
    return response

# Ruta para reporte Excel
@app.route('/reporte/propietarios/excel')
def exportar_propietarios_excel():
    datos = obtener_reporte_propietarios()
    if not datos:
        return "No hay datos para exportar", 404
    df = pd.DataFrame(datos)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Propietarios')
    output.seek(0)
    return send_file(
        output,
        download_name="reporte_propietarios.xlsx",
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

