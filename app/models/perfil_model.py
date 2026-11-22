"""Dados de perfil separados da autenticação e do histórico do IMC."""
from app.db import DatabaseConnection


class PerfilSaude:
    def __init__(self, id=None, usuario_id=None, data_nascimento=None,
                 sexo_calculo=None, nivel_atividade="nao_informado", objetivo="manter"):
        self.id = id
        self.usuario_id = usuario_id
        self.data_nascimento = data_nascimento
        self.sexo_calculo = sexo_calculo
        self.nivel_atividade = nivel_atividade
        self.objetivo = objetivo

    def salvar(self):
        """Cria ou atualiza o perfil, identificado pelo proprietário."""
        with DatabaseConnection() as db:
            db.cursor.execute("""
                INSERT INTO perfil_saude
                    (usuario_id, data_nascimento, sexo_calculo, nivel_atividade, objetivo)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(usuario_id) DO UPDATE SET
                    data_nascimento = excluded.data_nascimento,
                    sexo_calculo = excluded.sexo_calculo,
                    nivel_atividade = excluded.nivel_atividade,
                    objetivo = excluded.objetivo
            """, (self.usuario_id, self.data_nascimento, self.sexo_calculo,
                  self.nivel_atividade, self.objetivo))
            db.cursor.execute("SELECT id FROM perfil_saude WHERE usuario_id = ?", (self.usuario_id,))
            self.id = db.cursor.fetchone()["id"]
        return self

    @classmethod
    def buscar_por_usuario(cls, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM perfil_saude WHERE usuario_id = ?", (usuario_id,))
            row = db.cursor.fetchone()
        return cls(**dict(row)) if row else None
