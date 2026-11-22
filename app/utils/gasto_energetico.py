"""Estimativas energéticas educativas, nunca metas de ingestão.

12–17 anos: EER (necessidade energética estimada) com componente de
crescimento, segundo IOM/DRI 2006. 18+ anos: TMB Mifflin-St Jeor vezes
fator aproximado de atividade. Fontes no README.
"""
from datetime import date

FATORES_ATIVIDADE_ADULTOS = {"baixa": 1.2, "moderada": 1.55, "alta": 1.725}
# Coeficientes das equações DRI/IOM para idades de 9 a 18 anos.
# 'baixa': sedentário; 'moderada': ativo; 'alta': muito ativo.
FATORES_ATIVIDADE_ADOLESCENTES = {
    "masculino": {"baixa": 1.00, "moderada": 1.26, "alta": 1.42},
    "feminino": {"baixa": 1.00, "moderada": 1.31, "alta": 1.56},
}


def calcular_idade(data_nascimento, hoje=None):
    if not data_nascimento:
        return None
    hoje = hoje or date.today()
    nascimento = date.fromisoformat(data_nascimento)
    if nascimento > hoje:
        raise ValueError("Data de nascimento futura")
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))


def estimar_energia_diaria(perfil, ultimo_imc, hoje=None):
    """Retorna {valor, tipo, metodo}, ou None se os dados não permitirem estimar.

    Não retorna metas calóricas de alimentação, déficit ou superávit.
    O EER de adolescentes INCLUI necessidade adicional associada ao crescimento,
    portanto não é intercambiável com gasto metabólico medido.
    """
    if perfil is None or ultimo_imc is None or not perfil.data_nascimento:
        return None
    try:
        idade = calcular_idade(perfil.data_nascimento, hoje)
        peso = float(ultimo_imc.peso)
        altura_m = float(ultimo_imc.altura)
    except (ValueError, TypeError, OverflowError):
        return None
    if (idade is None or not 12 <= idade <= 120 or
            not 20 <= peso <= 400 or not 0.8 <= altura_m <= 2.7 or
            perfil.sexo_calculo not in ("feminino", "masculino") or
            perfil.nivel_atividade not in FATORES_ATIVIDADE_ADULTOS):
        return None

    if idade < 18:
        pa = FATORES_ATIVIDADE_ADOLESCENTES[perfil.sexo_calculo][perfil.nivel_atividade]
        if perfil.sexo_calculo == "masculino":
            eer = 88.5 - 61.9 * idade + pa * (26.7 * peso + 903 * altura_m) + 25
        else:
            eer = 135.3 - 30.8 * idade + pa * (10.0 * peso + 934 * altura_m) + 25
        if eer <= 0:
            return None
        return {"valor": round(eer), "tipo": "necessidade", "metodo": "DRI/IOM 2006 (12–17 anos)"}

    ajuste = -161 if perfil.sexo_calculo == "feminino" else 5
    tmb = 10 * peso + 6.25 * altura_m * 100 - 5 * idade + ajuste
    if tmb <= 0:
        return None
    return {
        "valor": round(tmb * FATORES_ATIVIDADE_ADULTOS[perfil.nivel_atividade]),
        "tipo": "gasto",
        "metodo": "Mifflin-St Jeor × atividade (adultos)",
    }


def estimar_gasto_adulto(perfil, ultimo_imc, hoje=None):
    """Compatibilidade com integrações antigas; retorna só valor adulto."""
    resultado = estimar_energia_diaria(perfil, ultimo_imc, hoje)
    return resultado["valor"] if resultado and resultado["tipo"] == "gasto" else None
