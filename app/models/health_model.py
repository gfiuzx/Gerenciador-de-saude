from app.db import DatabaseConnection
class IMCModel:
    def __init__(self,id=None,usuario_id=None,peso=None,altura=None,imc=None,classificacao=None,data_registro=None):
        self.id,self.usuario_id,self.peso,self.altura=id,usuario_id,peso,altura
        self.imc,self.classificacao,self.data_registro=imc,classificacao,data_registro
    @staticmethod
    def calcular_classificacao(v):
        if v<18.5:return "Abaixo do peso"
        if v<25:return "Peso normal"
        if v<30:return "Sobrepeso"
        if v<35:return "Obesidade Grau I"
        if v<40:return "Obesidade Grau II"
        return "Obesidade Grau III"
    def salvar(self):
        with DatabaseConnection() as db:
            if self.id is None:
                db.cursor.execute("INSERT INTO imc_registos(usuario_id,peso,altura,imc,classificacao) VALUES(?,?,?,?,?)",(self.usuario_id,self.peso,self.altura,self.imc,self.classificacao)); self.id=db.cursor.lastrowid
            else: db.cursor.execute("UPDATE imc_registos SET peso=?,altura=?,imc=?,classificacao=? WHERE id=? AND usuario_id=?",(self.peso,self.altura,self.imc,self.classificacao,self.id,self.usuario_id))
        return self
    @classmethod
    def buscar_por_usuario(cls,uid,busca=None):
        with DatabaseConnection() as db:
            sql="SELECT * FROM imc_registos WHERE usuario_id=?"; args=[uid]
            if busca: sql+=" AND classificacao LIKE ?"; args.append("%"+busca+"%")
            db.cursor.execute(sql+" ORDER BY data_registro DESC, id DESC",tuple(args)); rows=db.cursor.fetchall()
        return [cls(**dict(r)) for r in rows]
    @classmethod
    def buscar_por_id(cls,rid,uid):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM imc_registos WHERE id=? AND usuario_id=?",(rid,uid)); r=db.cursor.fetchone()
        return cls(**dict(r)) if r else None
    @classmethod
    def excluir(cls,rid,uid):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM imc_registos WHERE id=? AND usuario_id=?",(rid,uid)); return db.cursor.rowcount>0
class RefeicaoModel:
    def __init__(self,id=None,usuario_id=None,titulo=None,descricao=None,calorias=None,data_registro=None):
        self.id,self.usuario_id,self.titulo=id,usuario_id,titulo
        self.descricao,self.calorias,self.data_registro=descricao,calorias,data_registro
    def salvar(self):
        with DatabaseConnection() as db:
            if self.id is None:
                db.cursor.execute("INSERT INTO refeicoes(usuario_id,titulo,descricao,calorias) VALUES(?,?,?,?)",(self.usuario_id,self.titulo,self.descricao,self.calorias)); self.id=db.cursor.lastrowid
            else: db.cursor.execute("UPDATE refeicoes SET titulo=?,descricao=?,calorias=? WHERE id=? AND usuario_id=?",(self.titulo,self.descricao,self.calorias,self.id,self.usuario_id))
        return self
    @classmethod
    def buscar_por_usuario(cls,uid,busca=None):
        with DatabaseConnection() as db:
            sql="SELECT * FROM refeicoes WHERE usuario_id=?"; args=[uid]
            if busca: sql+=" AND (titulo LIKE ? OR descricao LIKE ?)"; args += ["%"+busca+"%","%"+busca+"%"]
            db.cursor.execute(sql+" ORDER BY data_registro DESC, id DESC",tuple(args)); rows=db.cursor.fetchall()
        return [cls(**dict(r)) for r in rows]
    @classmethod
    def buscar_por_periodo(cls, usuario_id, inicio_utc, fim_utc):
        """Refeições registradas no intervalo UTC [inicio_utc, fim_utc).

        Os registros SQLite usam CURRENT_TIMESTAMP, que armazena horário UTC.
        A conversão de data local para UTC é feita pelo Controller.
        """
        with DatabaseConnection() as db:
            db.cursor.execute(
                """SELECT * FROM refeicoes
                   WHERE usuario_id = ? AND data_registro >= ? AND data_registro < ?
                   ORDER BY data_registro ASC, id ASC""",
                (usuario_id, inicio_utc, fim_utc)
            )
            rows = db.cursor.fetchall()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def buscar_por_id(cls,rid,uid):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM refeicoes WHERE id=? AND usuario_id=?",(rid,uid)); r=db.cursor.fetchone()
        return cls(**dict(r)) if r else None
    @classmethod
    def excluir(cls,rid,uid):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM refeicoes WHERE id=? AND usuario_id=?",(rid,uid)); return db.cursor.rowcount>0
