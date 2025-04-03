from models.disciplina import Disciplina
from models.aluno import Aluno

class Nota:
    def __init__(self, disciplina: Disciplina, aluno: Aluno, valor: float, tipo: str, valor_max: float, matricula: int = None):
        self.__matricula: int = matricula
        self.__disciplina: Disciplina = disciplina
        self.__aluno: Aluno = aluno
        self.__valor: float = valor
        self.__tipo: str = tipo
        self.__valor_max: float = valor_max
    
    def get_matricula(self) -> int:
        return self.__matricula
    
    def set_matricula(self, matricula: int = None) -> None:
        self.__matricula = matricula
    
    def get_disciplina(self) -> Disciplina:
        return self.__disciplina
    
    def set_disciplina(self, disciplina: Disciplina) -> None:
        self.__disciplina = Disciplina
    
    def get_aluno(self) -> Aluno:
        return self.__aluno

    def set_aluno(self, aluno: Aluno):
        self.__aluno = aluno
    
    def get_valor(self) -> float:
        return self.__valor
    
    def set_valor(self, valor: float) -> None:
        self.__valor = valor
    
    def get_valor_max(self) -> float:
        return self.__valor_max
    
    def set_valor_max(self, valor_max: float) -> None:
        self.__valor_max = valor_max
    
    def get_tipo(self) -> str:
        return self.__tipo
    
    def set_tipo(self, tipo: str) -> None:
        self.__tipo = tipo
    
    def __repr__(self) -> str:
        return f"Nota('{self.__matricula}','{self.__disciplina.__repr__()}','{self.__aluno.__repr__()}','{self.__valor}','{self.__valor_max}','{self.__tipo}')"
    
    def __str__(self) -> str:
        return (
            "+------- Notas do Aluno -------+\n|\n"
            f"|  Matrícula:          {self.__matricula}\n"
            f"|  Disciplina:         {self.__disciplina.get_nome()}\n"
            f"|  Aluno:              {self.__aluno.get_nome()}\n"
            f"|  Valor:              {self.__data_nascimento}\n"
            f"|  Valor Maximo:       {self.__valor_max}\n"
            f"|  Tipo:               {self.__tipo}\n|\n"
            "+------------------------------+"
        )
    
