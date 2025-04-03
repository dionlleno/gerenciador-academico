from models.aluno import Aluno

class Disciplina:
    def __init__(self, turno: str, sala: str, nome: str, alunos: list[Aluno] = None, matricula: int = None):
        self.__matricula: int = matricula
        self.__turno: str = turno
        self.__sala: str = sala
        self.__nome: str = nome
        self.__alunos: list[Aluno] = alunos
    
    def get_matricula(self) -> int:
        return self.__matricula
    
    def set_matricula(self, matricula: int) -> None:
        self.__matricula = matricula
    
    def get_turno(self) -> str:
        return self.__turno
    
    def set_turno(self, turno: str) -> None:
        self.__turno = turno
    
    def get_sala(self) -> str:
        return self.__sala
    
    def set_sala(self, sala: str) -> None:
        self.__sala = sala
    
    def get_nome(self) -> str:
        return self.__nome
    
    def set_nome(self, nome: str) -> None:
        self.__nome = nome
    
    def get_alunos(self) -> list[Aluno]:
        return self.__alunos
    
    def set_alunos(self, alunos: list[Aluno]) -> None:
        self.alunos = alunos
    
    def __repr__(self) -> str:
        return f"Disciplina('{self.__matricula}', '{self.__nome}', '{self.__turno}', [{', '.join(aluno.__repr__() for aluno in self.__alunos)}])"
    
    def __str__(self) -> str:
        return (
            "+----- Dados da Disciplina -----+\n|\n"
            f"|  Matricula: {self.__matricula}\n"
            f"|  Nome:      {self.__nome}\n"
            f"|  Turno:     {self.__turno}\n"
            f"|  Sala:      {self.__sala}\n"
            f"|  Alunos:    \n"
            f"{''.join(str(aluno.__str__()) for aluno in self.__alunos)}"
            "|\n+-------------------------------+"
        )