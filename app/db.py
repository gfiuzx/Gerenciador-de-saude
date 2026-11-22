import os, sqlite3
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "banco_sistema.db")
class DatabaseConnection:
    def __init__(self, db_path=DB_PATH):
        self.db_path, self.conn, self.cursor = db_path, None, None
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.rollback() if exc_type else self.conn.commit()
        finally:
            if self.conn: self.conn.close()
        return False
