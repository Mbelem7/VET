from flask import request

from flask import redirect, render_template, session
from functools import wraps

#verificar si estas logueado
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function



#verifica si es administrador
def admin_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        roles = session.get("user_role") or []
        if "Adminvet" not in roles:
            return redirect("/")  # Redirigir si no tiene permiso

        return f(*args, **kwargs)

    return decorated_function




#verifica si es veterinario
def veterinario_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session.get("user_role"))
        roles = session.get("user_role") or []
        if "Veterinario" not in roles and "Adminvet" not in roles:
            return redirect("/")  # Redirigir si no tiene permiso

        return f(*args, **kwargs)

    return decorated_function




def vetRec_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        roles = session.get("user_role") or []
        if ("Veterinario" not in roles and "Recepcionista" not in roles and "Adminvet" not in roles):
            return redirect("/")  # Redirigir si no tiene permiso

        return f(*args, **kwargs)

    return decorated_function



#verifica si es recepcionista
def recepcionista_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        roles = session.get("user_role") or []
        if "Recepcionista" not in roles:
            # Si el usuario no tiene el rol de ADMIN, redirigir a la página de inicio
            return redirect("/")  # Redirigir si no tiene permiso

        return f(*args, **kwargs)

    return decorated_function