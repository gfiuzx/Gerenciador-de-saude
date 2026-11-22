from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection
class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None):
        self.id, self.nome, self.email, self.senha_hash = id, nome, email, senha_hash
    @property
    def username(self): return self.email
    def salvar(self):
        with DatabaseConnection() as db:
            if self.id is None:
                db.cursor.execute("INSERT INTO usuarios (nome,email,senha_hash) VALUES (?,?,?)",(self.nome,self.email,self.senha_hash))
                self.id=db.cursor.lastrowid
            else:
                db.cursor.execute("UPDATE usuarios SET nome=?,email=?,senha_hash=? WHERE id=?",(self.nome,self.email,self.senha_hash,self.id))
        return self
    def verificar_senha(self, senha): return check_password_hash(self.senha_hash, senha)
    @classmethod
    def buscar_por_email(cls,email):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE email=?",(email,)); row=db.cursor.fetchone()
        return cls(**dict(row)) if row else None
    @classmethod
    def buscar_por_id(cls,uid):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE id=?",(uid,)); row=db.cursor.fetchone()
        return cls(**dict(row)) if row else None
    query_filter_by_email = buscar_por_email
    @classmethod
    def criar_usuario(cls,nome,email,senha):
        return cls(nome=nome,email=email,senha_hash=generate_password_hash(senha)).salvar()
UserModel=Usuario
