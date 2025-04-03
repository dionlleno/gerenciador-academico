from repositories.disciplina_repository import DisciplinaRepository
from repositories.aluno_repository import AlunoRepository
from models.disciplina import Disciplina
from models.aluno import Aluno

class DisciplinaService:
    def __init__(self):
        self.repository = DisciplinaRepository()
        self.repository_aluno = AlunoRepository()
        self.disciplina = Disciplina(matricula=None,nome=None,turno=None,sala=None,alunos=[])
        self.disciplinas = list[Disciplina]
    
    def adicionar(self, nome: str, turno: str, sala: str, alunos: list[Aluno] = []) -> bool:
        if nome and turno and sala:
            nome = nome.upper().strip()
            turno = turno.upper().strip()
            sala = sala.upper().strip()
            alunos = alunos
            self.disciplina.set_nome(nome)
            self.disciplina.set_turno(turno)
            self.disciplina.set_sala(sala)
            self.disciplina.set_alunos(alunos)
            self.repository.adicionar(self.disciplina)
            return True
        else:
            return False
    
    def matricular(self, matricula_aluno, matricula_disciplina) -> str:
        return self.repository.matricular(matricula_aluno=matricula_aluno, matricula_disciplina=matricula_disciplina)
    
    def desmatricular(self, matricula_aluno, matricula_disciplina) -> str:
        return self.repository.desmatricular(matricula_aluno=matricula_aluno, matricula_disciplina=matricula_disciplina)
    
    def buscar_por_matricula(self, matricula: int) -> Disciplina:
        self.disciplina = self.repository.buscar_por_matricula(matricula)
        return self.disciplina if self.disciplina else None
    
    def buscar_por_nome(self, nome: str) -> list[Disciplina]:
        self.disciplinas = self.repository.buscar_por_nome(nome)
        return self.disciplinas if self.disciplinas else None
    
    def atualizar(self, matricula: int, nome: str, turno: str, sala: str,  alunos: list[Aluno] = None) -> None:
        nome = nome.upper().strip()
        turno = turno.upper().strip()
        sala = sala.upper().strip()
        alunos = alunos
        self.disciplina.set_matricula(matricula)
        self.disciplina.set_nome(nome)
        self.disciplina.set_turno(turno)
        self.disciplina.set_sala(sala)
        self.disciplina.set_alunos(alunos)
        self.repository.atualizar(self.disciplina)
    
    def excluir(self, matricula: int) -> None:
        self.repository.excluir(matricula=matricula)
    
    def listar(self) -> list[Disciplina]:
        self.disciplinas = self.repository.listar()
        if self.disciplinas: 
            return self.disciplinas
        return []
    
    def listar_matriculados(self, matricula) -> list[Aluno]:
        self.alunos = self.repository.listar_matriculados(matricula)
        if self.alunos: 
            return self.alunos
        return []