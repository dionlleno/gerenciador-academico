import sqlite3
from models.disciplina import Disciplina
from models.aluno import Aluno
from repositories.aluno_repository import AlunoRepository

class DisciplinaRepository:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabelas()
        self.repository = AlunoRepository()

    def _criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplina (
                matricula INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                turno TEXT NOT NULL,
                sala TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplina_aluno (
                disciplina_matricula INTEGER,
                aluno_matricula INTEGER,
                FOREIGN KEY (disciplina_matricula) REFERENCES disciplina (matricula),
                FOREIGN KEY (aluno_matricula) REFERENCES aluno (matricula),
                PRIMARY KEY (disciplina_matricula, aluno_matricula)
            )
        ''')
        self.conn.commit()

    def adicionar(self, disciplina: Disciplina):
        self.cursor.execute(
            "INSERT INTO disciplina (nome, turno, sala) VALUES (?, ?, ?)",
            (disciplina.get_nome(), disciplina.get_turno(), disciplina.get_sala())
        )
        self.conn.commit()
        
    def matricular(self, matricula_aluno: int, matricula_disciplina: int) -> None:
        self.cursor.execute(
            "SELECT COUNT(*) FROM disciplina_aluno WHERE disciplina_matricula = ? AND aluno_matricula = ?",
            (matricula_disciplina, matricula_aluno)
        )
        if self.cursor.fetchone()[0] > 0:
            return "O aluno já está matriculado nesta disciplina."
        self.cursor.execute(
            "INSERT INTO disciplina_aluno (disciplina_matricula, aluno_matricula) VALUES (?, ?)",
            (matricula_disciplina, matricula_aluno)
        )
        self.conn.commit()
        return "O aluno matriculado com sucesso."
    
    def desmatricular(self, matricula_aluno: int, matricula_disciplina: int) -> None:
        # Verifica se a matrícula existe
        self.cursor.execute(
            "SELECT COUNT(*) FROM disciplina_aluno WHERE disciplina_matricula = ? AND aluno_matricula = ?",
            (matricula_disciplina, matricula_aluno)
        )
        if self.cursor.fetchone()[0] == 0:
            return"O aluno não está matriculado nesta disciplina."

        # Se estiver matriculado, faz a remoção
        self.cursor.execute(
            "DELETE FROM disciplina_aluno WHERE disciplina_matricula = ? AND aluno_matricula = ?",
            (matricula_disciplina, matricula_aluno)
        )
        self.conn.commit()
        return "Aluno desmatriculado com sucesso!"
    
    def buscar_por_matricula(self, matricula: int) -> Disciplina:
            self.cursor.execute("SELECT * FROM disciplina WHERE matricula = ?", (matricula,))
            disciplina = self.cursor.fetchone()
            if disciplina:
                self.cursor.execute(
                    "SELECT aluno_matricula FROM disciplina_aluno WHERE disciplina_matricula = ?", (matricula,))
                alunos = []
                for matriculado in self.cursor.fetchall():
                    alunos.append(self.repository.obter_por_matricula(matriculado[0]))
                return Disciplina(matricula=disciplina[0], nome=disciplina[1], turno=disciplina[2], sala=disciplina[3], alunos=alunos)
            return None
    
    def buscar_por_nome(self, nome: str):
        self.cursor.execute("SELECT * FROM disciplina WHERE nome LIKE ? ORDER BY nome ASC", ("%"+nome+"%",))
        disciplinas = self.cursor.fetchall()
        if disciplinas:
            return [Disciplina(
                matricula=disciplina[0],
                nome=disciplina[1],
                turno=disciplina[2],
                sala=disciplina[3],
                alunos=[]) for disciplina in disciplinas]
                

    def atualizar(self, disciplina: Disciplina):
        self.cursor.execute(
            "UPDATE disciplina SET nome = ?, turno = ?, sala = ? WHERE matricula = ?",
            (disciplina.get_nome(), disciplina.get_turno(), disciplina.get_sala(), disciplina.get_matricula())
        )
        self.cursor.execute("DELETE FROM disciplina_aluno WHERE disciplina_matricula = ?", (disciplina.get_matricula(),))
        for aluno in disciplina.get_alunos():
            self.cursor.execute(
                "INSERT INTO disciplina_aluno (disciplina_matricula, aluno_matricula) VALUES (?, ?)",
                (disciplina.get_matricula(), aluno.get_matricula())
            )
        self.conn.commit()

    def excluir(self, matricula: int):
        self.cursor.execute("DELETE FROM disciplina_aluno WHERE disciplina_matricula = ?", (matricula,))
        self.cursor.execute("DELETE FROM disciplina WHERE matricula = ?", (matricula,))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM disciplina ORDER BY nome ASC")
        disciplinas = self.cursor.fetchall()
        if disciplinas:
            self.conn.commit()
            return [Disciplina(
                matricula=disciplina[0],
                nome=disciplina[1],
                turno=disciplina[2],
                sala=disciplina[3],
                alunos=[]) for disciplina in disciplinas]
            
    def listar_matriculados(self, matricula) -> list[Aluno]:
        self.cursor.execute(
            "SELECT aluno_matricula FROM disciplina_aluno WHERE disciplina_matricula = ?", (matricula,))
        alunos = []
        for matriculado in self.cursor.fetchall():
            alunos.append(self.repository.buscar_por_matricula(matriculado[0]))
        return alunos

    def fechar_conexao(self):
        self.conn.close()
