import sqlite3
from models.nota import Nota
from models.aluno import Aluno
from models.disciplina import Disciplina
from repositories.disciplina_repository import DisciplinaRepository
from repositories.aluno_repository import AlunoRepository

class NotaRepository:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nota (
                matricula INTEGER PRIMARY KEY,
                valor FLOAT NOT NULL,
                valor_max FLOAT NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nota_disciplina_aluno (
                nota_matricula INTEGER,
                disciplina_matricula INTEGER,
                aluno_matricula INTEGER,
                FOREIGN KEY (nota_matricula) REFERENCES nota (matricula),
                FOREIGN KEY (disciplina_matricula) REFERENCES disciplina (matricula),
                FOREIGN KEY (aluno_matricula) REFERENCES aluno (matricula),
                PRIMARY KEY (nota_matricula, disciplina_matricula, aluno_matricula)
            )
        ''')
        self.conn.commit()

    def adicionar(self, nota: Nota) -> None:
        with self.conn:
            self.cursor.execute(
                "INSERT INTO nota (valor, valor_max, tipo) VALUES (?, ?, ?)",
                (nota.get_valor(), nota.get_valor_max(), nota.get_tipo())
            )
            nota_matricula = self.cursor.lastrowid  # Pegar o último ID inserido
            self.cursor.execute(
                "INSERT INTO nota_disciplina_aluno (nota_matricula, disciplina_matricula, aluno_matricula) VALUES (?, ?, ?)",
                (nota_matricula, nota.get_disciplina().get_matricula(), nota.get_aluno().get_matricula())
            )

    def obter(self, matricula: int) -> Nota:
        self.cursor.execute("SELECT * FROM nota WHERE matricula = ?", (matricula,))
        nota = self.cursor.fetchone()
        if nota:
            print("NOTA - OBTER - ", nota)
            aluno = self.obter_aluno(matricula=matricula)
            disciplina = self.obter_disciplina(matricula=matricula)
            return Nota(matricula=nota[0], valor=nota[1], valor_max=nota[2], tipo=nota[3], disciplina=disciplina, aluno=aluno)
        return None
    
    def obter_aluno(self, matricula: int) -> Aluno:
        self.cursor.execute("SELECT aluno_matricula FROM nota_disciplina_aluno WHERE nota_matricula = ?", (matricula,))
        matricula_aluno = self.cursor.fetchone()
        print(matricula)
        repo_aluno = AlunoRepository()
        aluno = repo_aluno.obter(matricula_aluno)
        return aluno
    
    def obter_disciplina(self, matricula: int) -> Disciplina:
        self.cursor.execute("SELECT disciplina_matricula FROM nota_disciplina_aluno WHERE nota_matricula = ?", (matricula,))
        matricula_disciplina = self.cursor.fetchone()
        repo_disciplina = DisciplinaRepository()
        disciplina = repo_disciplina.obter(matricula_disciplina)
        return disciplina

    def atualizar(self, nota: Nota) -> None:
        with self.conn:
            self.cursor.execute(
                "UPDATE nota SET valor = ?, valor_max = ?, tipo = ? WHERE matricula = ?",
                (nota.get_valor(), nota.get_valor_max(), nota.get_tipo(), nota.get_matricula())
            )
            self.cursor.execute(
                "DELETE FROM nota_disciplina_aluno WHERE nota_matricula = ?",
                (nota.get_matricula(),)
            )
            self.cursor.execute(
                "INSERT INTO nota_disciplina_aluno (nota_matricula, disciplina_matricula, aluno_matricula) VALUES (?, ?, ?)",
                (nota.get_matricula(), nota.get_disciplina().get_matricula(), nota.get_aluno().get_matricula())
            )

    def excluir(self, matricula: int) -> None:
        with self.conn:
            self.cursor.execute("DELETE FROM nota_disciplina_aluno WHERE nota_matricula = ?", (matricula,))
            self.cursor.execute("DELETE FROM nota WHERE matricula = ?", (matricula,))

    def listar(self) -> list[Nota]:
        self.cursor.execute("SELECT * FROM nota")
        notas = []
        for nota in self.cursor.fetchall():
            print("NOTA - OBTER - ", nota)
            aluno = self.obter_aluno(nota[0])
            disciplina = self.obter_disciplina(nota[0])
            notas.append(Nota(matricula=nota[0], valor=nota[1], valor_max=nota[2], tipo=nota[3], disciplina=disciplina, aluno=aluno))
        return notas

    def fechar_conexao(self):
        self.conn.close()
