from repositories.aluno_repository import AlunoRepository
from models.aluno import Aluno

class AlunoService:
    def __init__(self):
        self.repository = AlunoRepository()
        self.aluno = Aluno(matricula=None,nome=None,data_nascimento=None)
        self.alunos = list[Aluno]

    def adicionar(self, nome: str, data_nascimento: str) -> bool:
        if nome and data_nascimento:
            nome = nome.upper().strip()
            data_nascimento = data_nascimento.strip()
            self.aluno.set_nome(nome)
            self.aluno.set_data_nascimento(data_nascimento)
            self.repository.adicionar(self.aluno)
            return True
        else: 
            return False
    
    def buscar_por_matricula(self, matricula: str) -> Aluno:
        matricula = matricula
        self.aluno = self.repository.buscar_por_matricula(matricula)
        return self.aluno if self.aluno else None
    
    def buscar_por_nome(self, nome: str) -> list[Aluno]:
        self.alunos = self.repository.buscar_por_nome(nome=nome)
        return self.alunos if self.alunos else None
    
    def atualizar(self, matricula: int, nome: str, data_nascimento: str) -> None:
        nome = nome.upper().strip()
        data_nascimento = data_nascimento.strip()
        self.aluno.set_matricula(matricula)
        self.aluno.set_nome(nome)
        self.aluno.set_data_nascimento(data_nascimento)
        self.repository.atualizar(self.aluno)
    
    def excluir(self, matricula: int) -> None:
        self.repository.excluir(matricula=matricula)
    
    def listar(self) -> list[Aluno]:
        self.alunos = self.repository.listar()
        if self.alunos: return self.alunos
        return []