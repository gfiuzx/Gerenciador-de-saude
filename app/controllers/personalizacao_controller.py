"""Preferências de interface com formulário Flask e cookies, sem JavaScript."""
from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash
from app.utils.auth_middleware import login_required

personalizacao_bp = Blueprint("personalizacao", __name__)

@personalizacao_bp.route("/personalizacao", methods=["GET", "POST"])
@login_required
def preferencias():
    if request.method == "POST":
        tema = request.form.get("tema", "claro")
        cor = request.form.get("cor", "verde")
        densidade = request.form.get("densidade", "confortavel")
        if tema not in ("claro", "escuro") or cor not in ("verde", "azul", "roxo", "laranja") or densidade not in ("confortavel", "compacto"):
            flash("Confira as opções de aparência selecionadas.", "danger")
            return redirect(url_for("personalizacao.preferencias"))
        resposta = make_response(redirect(url_for("personalizacao.preferencias")))
        for nome, valor in (("theme", "dark" if tema == "escuro" else "light"), ("accent", cor), ("density", densidade)):
            resposta.set_cookie(nome, valor, max_age=31536000, httponly=True, samesite="Lax")
        flash("Preferências de aparência salvas.", "success")
        return resposta
    return render_template("personalizacao.html")
