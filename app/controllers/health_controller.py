from flask import Blueprint,request,redirect,url_for,flash,g,current_app,render_template,make_response
from app.models.health_model import IMCModel,RefeicaoModel
from app.utils.auth_middleware import login_required
health_bp=Blueprint("health",__name__,url_prefix="/saude")
def back(pagina="dashboard"):
    destinos = {
        "dashboard": "auth.dashboard",
        "imc": "auth.pagina_imc",
        "refeicoes": "auth.pagina_refeicoes", "perfil": "perfil.editar_perfil",
    }
    return redirect(url_for(destinos.get(pagina, "auth.dashboard")))
@health_bp.route("/calcular-imc",methods=["POST"])
@login_required
def calcular_imc():
    try:
        p=float(request.form.get("peso","")); a=float(request.form.get("altura",""))
        if not 20<=p<=400 or not .5<=a<=2.7: raise ValueError
        v=round(p/a**2,2); m=IMCModel(usuario_id=g.usuario.id,peso=p,altura=a,imc=v,classificacao=IMCModel.calcular_classificacao(v)).salvar()
        current_app.logger.info("IMC criado usuario_id=%s registro_id=%s",g.usuario.id,m.id); flash("IMC registrado: %s (%s)."%(v,m.classificacao),"success")
    except (ValueError,TypeError): flash("Peso deve estar entre 20 e 400 kg e altura entre 0,50 e 2,70 m.","danger")
    return back("imc")
@health_bp.route("/imc/<int:rid>/excluir",methods=["POST"])
@login_required
def excluir_imc(rid):
    flash("Registro de IMC excluído." if IMCModel.excluir(rid,g.usuario.id) else "Registro não encontrado ou sem permissão.","success"); return back("imc")
@health_bp.route("/imc/<int:rid>/editar",methods=["GET","POST"])
@login_required
def editar_imc(rid):
    m=IMCModel.buscar_por_id(rid,g.usuario.id)
    if not m: flash("Registro não encontrado.","danger"); return back("imc")
    if request.method=="POST":
        try:
            p=float(request.form.get("peso","")); a=float(request.form.get("altura",""))
            if not 20<=p<=400 or not .5<=a<=2.7: raise ValueError
            m.peso,m.altura=p,a; m.imc=round(p/a**2,2); m.classificacao=IMCModel.calcular_classificacao(m.imc); m.salvar()
            flash("IMC atualizado.","success"); return back("imc")
        except (ValueError,TypeError): flash("Valores inválidos.","danger")
    return render_template("editar_imc.html",registro=m)
@health_bp.route("/criar-refeicao",methods=["POST"])
@login_required
def criar_refeicao():
    titulo=(request.form.get("titulo") or "").strip(); desc=(request.form.get("descricao") or "").strip()
    try:
        cal=float(request.form.get("calorias") or 0)
        if not titulo or len(titulo)>100 or len(desc)>500 or not 0<=cal<=10000: raise ValueError
        r=RefeicaoModel(usuario_id=g.usuario.id,titulo=titulo,descricao=desc,calorias=cal).salvar()
        current_app.logger.info("Refeição criada usuario_id=%s registro_id=%s",g.usuario.id,r.id); flash("Refeição cadastrada.","success")
    except (ValueError,TypeError): flash("Título obrigatório (até 100 caracteres), descrição até 500 e calorias de 0 a 10.000.","danger")
    return back("refeicoes")
@health_bp.route("/refeicao/<int:rid>/excluir",methods=["POST"])
@login_required
def excluir_refeicao(rid):
    flash("Refeição excluída." if RefeicaoModel.excluir(rid,g.usuario.id) else "Refeição não encontrada ou sem permissão.","success"); return back("refeicoes")
@health_bp.route("/refeicao/<int:rid>/editar",methods=["GET","POST"])
@login_required
def editar_refeicao(rid):
    r=RefeicaoModel.buscar_por_id(rid,g.usuario.id)
    if not r: flash("Refeição não encontrada.","danger"); return back("refeicoes")
    if request.method=="POST":
        titulo=(request.form.get("titulo") or "").strip(); desc=(request.form.get("descricao") or "").strip()
        try:
            cal=float(request.form.get("calorias") or 0)
            if not titulo or len(titulo)>100 or len(desc)>500 or not 0<=cal<=10000: raise ValueError
            r.titulo,r.descricao,r.calorias=titulo,desc,cal; r.salvar(); flash("Refeição atualizada.","success"); return back("refeicoes")
        except (ValueError,TypeError): flash("Confira os campos informados.","danger")
    return render_template("editar_refeicao.html",item=r)
@health_bp.route("/preferencia-tema",methods=["POST"])
def preferencia_tema():
    tema=request.form.get("theme","light"); tema=tema if tema in ("light","dark") else "light"
    pagina = request.form.get("pagina", "dashboard")
    resp=make_response(back(pagina)); resp.set_cookie("theme",tema,max_age=31536000,httponly=True,samesite="Lax"); return resp
