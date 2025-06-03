from flask import Flask, render_template, request, redirect, session, jsonify
from modulos.helpers import *
from modulos.usuarios import buscarUsuario, rolesPorUsuario
from flask_session import Session
# form modulos.productos import *

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


@app.route('/mascotas')
@login_required
@veterinario_required
def mascotas():
   return render_template ('mascotas.html')


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

@app.route('/logout')
def logout():
      """Log user out."""
      # Forget any user_id
      session.clear()
   
      # Redirect user to login form
      return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)