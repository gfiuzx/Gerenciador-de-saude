"""Inicializa as tabelas e usuários de demonstração (exigência do projeto final).

Pode ser executado diretamente: python iniciar_bd.py
Execute antes de iniciar a aplicação com run.py.
"""
from werkzeug.security import generate_password_hash
from app.db import DatabaseConnection
from app.models.user_model import Usuario


def inicializar_banco():
    with DatabaseConnection() as db:

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
        """)

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS imc_registos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                peso REAL NOT NULL,
                altura REAL NOT NULL,
                imc REAL NOT NULL,
                classificacao TEXT NOT NULL,
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id)
                    REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS refeicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                calorias REAL DEFAULT 0,
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(usuario_id)
                    REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS perfil_saude (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL UNIQUE,
                data_nascimento DATE,
                sexo_calculo TEXT,
                nivel_atividade TEXT NOT NULL DEFAULT 'nao_informado',
                objetivo TEXT NOT NULL DEFAULT 'manter',
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)

        db.cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
        total = db.cursor.fetchone()["total"]

    if total == 0:
        Usuario(
            nome="João Silva",
            email="joao@teste.com",
            senha_hash=generate_password_hash("123456")
        ).salvar()

        Usuario(
            nome="Maria Souza",
            email="maria@teste.com",
            senha_hash=generate_password_hash("senha123")
        ).salvar()



if __name__ == "__main__":
    inicializar_banco()
    print("Banco inicializado com sucesso.")
