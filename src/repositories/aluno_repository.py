import sqlite3
from models.aluno import Aluno

class AlunoRepository:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aluno (
                matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                nome CHAR(50) NOT NULL,
                data_nascimento TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aluno_nota (
                aluno_matricula INTEGER,
                nota_matricula INTEGER,
                FOREIGN KEY (aluno_matricula) REFERENCES aluno (matricula) ON DELETE CASCADE,
                FOREIGN KEY (nota_matricula) REFERENCES nota (matricula) ON DELETE CASCADE,
                PRIMARY KEY (aluno_matricula, nota_matricula)
            )
        ''')
        self.conn.commit()
    
    def adicionar(self, aluno: Aluno):
        with self.conn:
            self.cursor.execute(
                "INSERT INTO aluno (nome, data_nascimento) VALUES (?, ?)",
                (aluno.get_nome(), aluno.get_data_nascimento())
            )

    def buscar_por_matricula(self, matricula: int) -> Aluno:
        self.cursor.execute("SELECT * FROM aluno WHERE matricula = ?", (matricula,))
        aluno = self.cursor.fetchone()
        if aluno:
            return Aluno(matricula=aluno[0], nome=aluno[1], data_nascimento=aluno[2])
        return None
    
    def buscar_por_nome(self, nome: str) -> list[Aluno]:
        self.cursor.execute("SELECT * FROM aluno WHERE nome LIKE ? ORDER BY nome ASC", ("%"+nome+"%",))
        alunos = self.cursor.fetchall()
        if alunos:
            return [Aluno(matricula=aluno[0], nome=aluno[1], data_nascimento=aluno[2]) for aluno in alunos]
        return None
    
    def atualizar(self, aluno: Aluno):
        with self.conn:
            self.cursor.execute(
                "UPDATE aluno SET nome = ?, data_nascimento = ? WHERE matricula = ?",
                (aluno.get_nome(), aluno.get_data_nascimento(), aluno.get_matricula())
            )

    def excluir(self, matricula: int):
        with self.conn:
            self.cursor.execute("DELETE FROM aluno_nota WHERE aluno_matricula = ?", (matricula,))
            self.cursor.execute("DELETE FROM aluno WHERE matricula = ?", (matricula,))

    def listar(self):
        self.cursor.execute("SELECT * FROM aluno ORDER BY nome ASC")
        alunos = self.cursor.fetchall()
        if alunos:
            return [Aluno(matricula=aluno[0], nome=aluno[1], data_nascimento=aluno[2]) for aluno in alunos]
        return None
    
    def fechar_conexao(self):
        self.conn.close()
