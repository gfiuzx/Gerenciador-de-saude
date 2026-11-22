from functools import wraps
from flask import g, session, redirect, url_for, flash, request
from app.models.user_model import Usuario
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user_id = session.get("user_id")
        usuario = Usuario.buscar_por_id(user_id) if user_id else None
        if usuario is None:
            session.clear()
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        g.usuario = usuario
        return view(*args, **kwargs)
    return wrapped
def registrar_middlewares(app):
    @app.before_request
    def carregar_usuario():
        g.usuario = None
        uid = session.get("user_id")
        if uid:
            g.usuario = Usuario.buscar_por_id(uid)
            if g.usuario is None: session.clear()
