from repositories.nota_repository import NotaRepository
from models.nota import Nota
from models.disciplina import Disciplina
from models.aluno import Aluno

class NotaService:
    def __init__(self):
        self.repo = NotaRepository()

    def adicionar_nota(self, valor: float, valor_max: float, tipo: str, matricula_disciplina: int, matricula_aluno: int):
        # Criando objetos disciplina e aluno fictícios (poderiam vir de repositórios)
        disciplina = Disciplina(matricula=matricula_disciplina, nome="Matemática", turno="Manhã", sala="101")
        aluno = Aluno(matricula=matricula_aluno, nome="João", data_nascimento="2000-05-15")
        
        # Criando a nota
        nota = Nota(valor=valor, valor_max=valor_max, tipo=tipo, disciplina=disciplina, aluno=aluno)
        self.repo.adicionar(nota)
    
    def listar_notas(self):
        return self.repo.listar()
    
    def atualizar_nota(self, matricula: int, valor: float, valor_max: float, tipo: str, matricula_disciplina: int, matricula_aluno: int):
        # Criando objetos disciplina e aluno fictícios (poderiam vir de repositórios)
        disciplina = Disciplina(matricula=matricula_disciplina, nome="Matemática", turno="Manhã", sala="101")
        aluno = Aluno(matricula=matricula_aluno, nome="João", data_nascimento="2000-05-15")
        
        # Criando a nota
        nota = Nota(matricula=matricula, valor=valor, valor_max=valor_max, tipo=tipo, disciplina=disciplina, aluno=aluno)
        self.repo.atualizar(nota)
    
    def excluir_nota(self, matricula: int):
        self.repo.excluir(matricula)
    
    def fechar_conexao(self):
        self.repo.fechar_conexao()
