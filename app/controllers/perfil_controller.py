"""Formulário de perfil de saúde: Flask e HTML, sem JavaScript."""
from datetime import date
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from app.models.perfil_model import PerfilSaude
from app.utils.auth_middleware import login_required
from app.utils.gasto_energetico import calcular_idade

perfil_bp = Blueprint("perfil", __name__)
OBJETIVOS = {"manter", "acompanhar_ganho", "acompanhar_perda"}
ATIVIDADES = {"nao_informado", "baixa", "moderada", "alta"}
SEXO_EQUACAO = {"nao_informado", "feminino", "masculino"}


@perfil_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def editar_perfil():
    perfil = PerfilSaude.buscar_por_usuario(g.usuario.id)
    if request.method == "POST":
        nascimento = (request.form.get("data_nascimento") or "").strip()
        sexo = (request.form.get("sexo_calculo") or "nao_informado").strip()
        atividade = (request.form.get("nivel_atividade") or "nao_informado").strip()
        objetivo = (request.form.get("objetivo") or "manter").strip()
        try:
            idade = calcular_idade(nascimento, date.today()) if nascimento else None
            if (idade is not None and not 0 <= idade <= 120) or (nascimento and not 1900 <= int(nascimento[:4]) <= date.today().year):
                raise ValueError
            if sexo not in SEXO_EQUACAO or atividade not in ATIVIDADES or objetivo not in OBJETIVOS:
                raise ValueError
        except (ValueError, TypeError):
            flash("Confira a data de nascimento e as opções selecionadas.", "danger")
        else:
            perfil = perfil or PerfilSaude(usuario_id=g.usuario.id)
            perfil.data_nascimento = nascimento or None
            perfil.sexo_calculo = None if sexo == "nao_informado" else sexo
            perfil.nivel_atividade = atividade
            perfil.objetivo = objetivo
            perfil.salvar()
            flash("Perfil atualizado com sucesso.", "success")
            return redirect(url_for("auth.dashboard"))
    return render_template("perfil.html", perfil=perfil)
