from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo
from flask import Blueprint,render_template,request,redirect,url_for,session,flash,current_app,g
from werkzeug.security import generate_password_hash
from app.models.user_model import Usuario
from app.models.health_model import IMCModel,RefeicaoModel
from app.models.perfil_model import PerfilSaude
from app.utils.gasto_energetico import estimar_energia_diaria, calcular_idade
from app.utils.auth_middleware import login_required
auth_bp=Blueprint("auth",__name__)
@auth_bp.route("/")
def index(): return redirect(url_for("auth.dashboard") if session.get("user_id") else url_for("auth.login"))
@auth_bp.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=(request.form.get("email") or "").strip().lower(); senha=request.form.get("senha") or ""
        usuario=Usuario.buscar_por_email(email) if email and len(email)<=120 else None
        if usuario and usuario.verificar_senha(senha):
            session.clear(); session["user_id"]=usuario.id; session["username"]=usuario.email; session["nome_usuario"]=usuario.nome
            current_app.logger.info("Login realizado usuario_id=%s",usuario.id); flash("Login realizado!","success")
            return redirect(url_for("auth.dashboard"))
        current_app.logger.warning("Falha de autenticação email=%s",email); flash("E-mail ou senha inválidos.","danger")
    return render_template("login.html")
@auth_bp.route("/cadastro",methods=["GET","POST"])
def cadastro():
    if request.method=="POST":
        nome=(request.form.get("nome") or "").strip(); email=(request.form.get("email") or "").strip().lower()
        senha=request.form.get("senha") or ""; conf=request.form.get("confirmar_senha") or ""
        if not nome or len(nome)>100 or "@" not in email or len(email)>120: flash("Informe nome e e-mail válidos.","danger")
        elif len(senha)<6 or len(senha)>128: flash("A senha deve ter entre 6 e 128 caracteres.","danger")
        elif senha!=conf: flash("As senhas não coincidem.","danger")
        elif Usuario.buscar_por_email(email): flash("E-mail já cadastrado.","danger")
        else:
            u=Usuario(nome=nome,email=email,senha_hash=generate_password_hash(senha)).salvar()
            current_app.logger.info("Cadastro usuario_id=%s",u.id); flash("Cadastro realizado. Faça login.","success")
            return redirect(url_for("auth.login"))
    return render_template("cadastro.html")
@auth_bp.route("/dashboard")
@login_required
def dashboard():
    # O banco grava CURRENT_TIMESTAMP em UTC; a rotina diária é calculada
    # no fuso de São Paulo para não misturar refeições de dias diferentes.
    fuso = ZoneInfo("America/Sao_Paulo")
    hoje = datetime.now(fuso).date()
    inicio_local = datetime.combine(hoje, time.min, tzinfo=fuso)
    fim_local = datetime.combine(hoje + timedelta(days=1), time.min, tzinfo=fuso)
    inicio_utc = inicio_local.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    fim_utc = fim_local.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    imcs = IMCModel.buscar_por_usuario(g.usuario.id)
    refeicoes_hoje = RefeicaoModel.buscar_por_periodo(
        g.usuario.id, inicio_utc, fim_utc
    )
    rotina_hoje = []
    for refeicao in refeicoes_hoje:
        # Os valores de data_registro gerados pelo SQLite estão em UTC.
        horario_utc = datetime.strptime(refeicao.data_registro, "%Y-%m-%d %H:%M:%S")
        horario_local = horario_utc.replace(tzinfo=timezone.utc).astimezone(fuso)
        rotina_hoje.append({"refeicao": refeicao, "hora": horario_local.strftime("%H:%M")})

    total_kcal_hoje = round(sum((r.calorias or 0) for r in refeicoes_hoje), 1)
    perfil = PerfilSaude.buscar_por_usuario(g.usuario.id)
    ultimo_imc = imcs[0] if imcs else None
    energia_estimada = estimar_energia_diaria(perfil, ultimo_imc, hoje)
    idade = calcular_idade(perfil.data_nascimento, hoje) if perfil and perfil.data_nascimento else None
    return render_template(
        "dashboard.html",
        nome=g.usuario.nome,
        data_hoje=hoje.strftime("%d/%m/%Y"),
        ultimo_imc=ultimo_imc,
        perfil=perfil,
        idade=idade,
        energia_estimada=energia_estimada,
        total_refeicoes_hoje=len(refeicoes_hoje),
        total_kcal_hoje=total_kcal_hoje,
        rotina_hoje=rotina_hoje,
    )

@auth_bp.route("/imc")
@login_required
def pagina_imc():
    imcs = IMCModel.buscar_por_usuario(g.usuario.id)
    return render_template("imc.html", historico_imc=imcs)

@auth_bp.route("/refeicoes")
@login_required
def pagina_refeicoes():
    refs = RefeicaoModel.buscar_por_usuario(g.usuario.id)
    return render_template("refeicoes.html", refeicoes=refs)

@auth_bp.route("/logout",methods=["GET","POST"])
def logout():
    session.clear(); flash("Você saiu do sistema.","info"); return redirect(url_for("auth.login"))
